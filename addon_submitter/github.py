# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com
"""Functions for working with GitHub pull requests"""

import os
import logging
import requests
import shutil
import subprocess
from pprint import pformat
from typing import List, NamedTuple
from django.conf import settings
from django.template.loader import render_to_string
from .zip_file import ZippedAddon

__all__ = ['prepare_repository', 'open_pull_request',
           'post_comment', 'GitHubError', 'PullRequestResult']

REPO_URL_MASK = 'https://{gh_token}@github.com/{user}/{repo}.git'
GH_API = 'https://api.github.com'
PR_ENPDOINT = '/repos/{user}/{repo}/pulls'
COMMENT_ENDPOINT = '/repos/{user}/{repo}/issues/{number}/comments'
GH_TOKEN = settings.GH_TOKEN

PullRequestResult = NamedTuple(
    'PullRequestResult',
    [('number', int), ('html_url', str)]
)


class GitHubError(Exception):
    pass


def _execute(args: List[str]) -> None:
    """
    Execute a console command

    :param args: a command with arguments
    :raises subprocess.CalledProcessError: if command returns non-0 code
    """
    res = subprocess.run(args,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    logging.debug('Subprocess run result: {0}'.format(res))
    res.check_returncode()


def _create_addon_directory(workdir: str, zipaddon: ZippedAddon) -> None:
    """
    Create a directory for addon

    :param workdir: working directory
    :param zipaddon: zipped addon
    """
    if not zipaddon.is_folder:
        os.chdir(workdir)
        addon_dir = os.path.join(workdir, zipaddon.id)
        os.mkdir(addon_dir)
    else:
        addon_dir = workdir
    zipaddon.extract(addon_dir)


def _prepare_pr_branch(repo: str, branch: str, workdir: str,
                       addon_id: str, addon_version: str,
                       new_pull_request: bool) -> None:
    """
    Create a git branch for pull request

    :param repo: addon repository name
    :param branch: branch to submit the addon to
    :param workdir: working directory
    :param addon_id: addon ID
    :param addon_version: addon version
    :param new_pull_request: is the PR new or old one
    """
    os.chdir(workdir)
    repo_url = REPO_URL_MASK.format(
        gh_token=GH_TOKEN,
        user= settings.PROXY_USER,
        repo=repo
    )
    _execute(['git', 'clone', repo_url])
    os.chdir(repo)
    _execute(['git', 'config', 'user.name', settings.USER_NAME])
    _execute(['git', 'config', 'user.email', settings.USER_EMAIL])
    if new_pull_request:
        _execute(['git', 'remote', 'add', 'upstream',
                 'https://github.com/{user}/{repo}.git'.format(
                     user=settings.UPSTREAM_USER,
                     repo=repo
                 )])
        _execute(['git', 'fetch', 'upstream'])
        _execute(['git', 'checkout', '-b', branch, '--track',
                 'origin/{0}'.format(branch)])
        _execute(['git', 'merge', 'upstream/{0}'.format(branch)])
        os.system('git branch -D ' + addon_id)
        _execute(['git', 'checkout', '-b', addon_id])
        shutil.rmtree(os.path.join(workdir, repo, addon_id), ignore_errors=True)
        shutil.copytree(os.path.join(workdir, addon_id),
                        os.path.join(workdir, repo, addon_id))
        _execute(['git', 'add', '--all', '.'])
        _execute(['git', 'commit', '-m', '"[{addon}] {version}"'.format(
            addon=addon_id,
            version=addon_version)
                  ])
    else:
        _execute(['git', 'checkout', addon_id])
        shutil.rmtree(os.path.join(workdir, repo, addon_id), ignore_errors=True)
        shutil.copytree(os.path.join(workdir, addon_id),
                        os.path.join(workdir, repo, addon_id))
        _execute(['git', 'add', '--all', '.'])
        _execute(['git', 'commit', '--amend', '--no-edit'])
    _execute(['git', 'push', '-f', 'origin', addon_id])


def prepare_repository(zipped_addon: ZippedAddon,
                       repo: str, branch: str, new_pull_request: bool) -> None:
    """
    Prepare the proxy repository for submitting a pull request

    :param zipped_addon: zipped addon
    :param repo: addon repository name
    :param branch: git branch (Kodi version codename)
    :param new_pull_request: is the PR new or old one
    """
    os.chdir(settings.WORKDIR)
    _execute(['mkdir', zipped_addon.md5])
    workdir = os.path.join(settings.WORKDIR, zipped_addon.md5)
    logging.debug('Workdir: {0}'.format(workdir))
    try:
        _create_addon_directory(workdir, zipped_addon)
        _prepare_pr_branch(repo, branch, workdir,
                           zipped_addon.id,
                           zipped_addon.version,
                           new_pull_request)
    except Exception:
        logging.exception('Error while preparing pull request!')
        raise
    finally:
        shutil.rmtree(workdir)


def open_pull_request(repo: str, branch: str,
                      addon_id: str,
                      addon_version: str,
                      addon_author: str,
                      source_url: str,
                      description: str) -> PullRequestResult:
    """
    Open a pull request on GitHub

    :param repo: addon repository
    :param branch: Git branch (Kodi version codename)
    :param addon_id: addon ID
    :param addon_version: addon version
    :param addon_author: addon author
    :param source_url: source code URL
    :param description: PR description
    :raises GitHubError: when failed to create a PR
    :return: Pull request # and URL
    """
    url = GH_API + PR_ENPDOINT.format(
        user=settings.UPSTREAM_USER,
        repo=repo
    )
    payload = {
        'title': '[{addon}] {version}'.format(
            addon=addon_id,
            version=addon_version),
        'head': '{user}:{branch}'.format(
            user=settings.PROXY_USER,
            branch=addon_id
        ),
        'base': branch,
        'body': render_to_string('addon_submitter/pr-comment.md',
                                 {'author': addon_author,
                                  'source_url': source_url,
                                  'description': description})
    }
    resp = requests.post(url, json=payload,
                         auth=(settings.PROXY_USER, GH_TOKEN))
    content = resp.json()
    if resp.status_code != 201:
        logging.error('GitHub response: {resp}: {content}'.format(
            resp=resp,
            content=pformat(content)
        ))
        raise GitHubError(
            'Failed to create a pull request with status code {0}!'.format(
                resp.status_code)
        )
    return PullRequestResult(content['number'], content['html_url'])


def post_comment(repo: str, pull_request_number: int, comment: str) -> None:
    """
    Post a comment to GitHub pull request

    :param repo: GitHub repository
    :param pull_request_number: pull request number
    :param comment: comment text
    """
    url = GH_API + COMMENT_ENDPOINT.format(
        user=settings.UPSTREAM_USER,
        repo=repo,
        number=pull_request_number
    )
    resp = requests.post(url,
                         json={'body': comment},
                         auth=(settings.PROXY_USER, GH_TOKEN))
    if resp.status_code != 201:
        logging.error('GitHub response: {resp}: {content}'.format(
            resp=resp,
            content=pformat(resp.json())
        ))
        raise GitHubError(
            'Failed to post a comment to a PR with status code {0}!'.format(
                resp.status_code)
        )
