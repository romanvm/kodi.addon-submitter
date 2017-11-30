# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com
"""Functions for working with GitHub pull requests"""

import os
import logging
import requests
import shutil
import subprocess
import sys
from pprint import pformat
from django.conf import settings
from addon_submitter.zip_file import ZippedAddon

REPO_URL_MASK = 'https://{gh_token}@github.com/{user}/{repo}.git'
GH_API = 'https://api.github.com'
PR_ENPDOINT = '/repos/{user}/{repo}/pulls'
COMMENT_ENDPOINT = '/repos/{user}/{repo}/issues/{number}/comments'
GH_TOKEN = os.environ['GH_TOKEN']

logger = logging.getLogger(__name__)
if settings.DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO
logger.setLevel(level)


class GitHubError(Exception):
    pass


def execute(args: list) -> None:
    """
    Execute a console command

    :param args: command with arguments
    :raises RuntimeError: if command returns non-0 code
    """
    call_string = ' '.join(args)
    logging.debug('Executing: ' + call_string)
    res = subprocess.call(args, shell=True)
    if res:
        raise RuntimeError('Call {call} returned error code {res}!'.format(
            call=call_string,
            res=res
        ))


def create_addon_directory(workdir: str, zipaddon: ZippedAddon) -> None:
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


def prepare_pr_branch(repo: str, branch: str, workdir: str,
                      addon_id: str, addon_version: str) -> None:
    """
    Create a git branch for pull request

    :param repo: addon repository name
    :param branch: branch to submit the addon to
    :param workdir: working directory
    :param addon_id: addon ID
    :param addon_version: addon version
    """
    os.chdir(workdir)
    repo_url = REPO_URL_MASK.format(
        gh_token=GH_TOKEN,
        user= settings.PROXY_USER,
        repo=repo
    )
    execute(['git', 'clone', repo_url])
    os.chdir(repo)
    execute(['git', 'config', 'user.name', settings.USER_NAME])
    execute(['git', 'config', 'user.email', settings.USER_EMAIL])
    execute(['git', 'remote', 'add', 'upstream',
             'https://github.com/{user}/{repo}.git'.format(
                 user=settings.UPSTREAM_USER,
                 repo=repo
             )])
    execute(['git', 'fetch', 'upstream'])
    execute(['git', 'checkout', '-b', branch, '--track',
             'origin/{0}'.format(branch)])
    execute(['git', 'merge', 'upstream/{0}'.format(branch)])
    os.system('git branch -D ' + addon_id)
    execute(['git', 'checkout', '-b', addon_id])
    shutil.rmtree(os.path.join(workdir, repo, addon_id), ignore_errors=True)
    shutil.copytree(os.path.join(workdir, addon_id),
                    os.path.join(workdir, repo, addon_id))
    execute(['git', 'add', '--all', '.'])
    execute(['git', 'commit', '-m', '"[{addon}] {version}"'.format(
        addon=addon_id,
        version=addon_version)
             ])
    execute(['git', 'push', '-f', 'origin', addon_id])


def prepare_repository(zipaddon: ZippedAddon, repo: str, branch: str) -> None:
    """
    Prepare the proxy repository for submitting a pull request

    :param zipaddon: zipped addon
    :param repo: addon repository name
    :param branch: git branch (Kodi version codename)
    """
    workdir = settings.WORKDIR
    try:
        create_addon_directory(workdir, zipaddon)
        prepare_pr_branch(repo, branch, workdir, zipaddon.id, zipaddon.version)
    except Exception:
        logging.exception('Error while preparing pull request!')
        raise
    finally:
        os.chdir(workdir)
        if sys.platform == 'win32':
            os.system('attrib -h -s /s')
            os.system('rd {0} /s /q'.format(os.path.join(workdir, repo)))
            os.system('rd {0} /s /q'.format(os.path.join(workdir, zipaddon.id)))
        else:
            shutil.rmtree(os.path.join(workdir, repo), ignore_errors=True)
            shutil.rmtree(os.path.join(workdir, zipaddon.id), ignore_errors=True)


def post_comment(repo: str, pr_number: int, comment: str) -> None:
    """
    Post a comment to GitHub pull request

    :param repo: GitHub repository
    :param pr_number: pull request number
    :param comment: comment text
    """
    url = GH_API + COMMENT_ENDPOINT.format(
        user=settings.UPSTREAM_USER,
        repo=repo,
        number=pr_number
    )
    resp = requests.post(url,
                         json={'body': comment},
                         auth=(settings.PROXY_USER, GH_TOKEN))
    logger.debug('GitHub response: {resp}: {content}'.format(
        resp=resp,
        content=pformat(resp.json())
    ))
    if resp.status_code != 201:
        raise GitHubError(
            'Failed to post a comment to a PR with status code {0}!'.format(
                resp.status_code)
        )


def open_pull_request(repo: str, branch: str, addon_id: str,
                      addon_version: str, description: str) -> int:
    """
    Open a pull request on GitHub

    :param repo: addon repository
    :param branch: Git branch (Kodi version codename)
    :param addon_id: addon ID
    :param addon_version: addon version
    :param description: PR description
    :raises GitHubError: when failed to create a PR
    :return: Pull request #
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
        'body': description
    }
    resp = requests.post(url, json=payload, auth=(settings.PROXY_USER, GH_TOKEN))
    content = resp.json()
    logger.debug('GitHub response: {resp}: {content}'.format(
        resp=resp,
        content=pformat(content)
    ))
    if resp.status_code != 201:
        raise GitHubError(
            'Failed to create a pull request with status code {0}!'.format(
                resp.status_code)
        )
    return content['number']


def main():
    import sys
    sys.path.append(settings.BASE_DIR)
    repo = 'repo-scripts'
    branch = 'krypton'
    addon = 'plugin.video.example-2.2.0.zip'
    description = 'Please accept this cool new addon to the repository'
    with open(os.path.join(settings.BASE_DIR,
                           'test_data', addon), 'rb') as fo:
        zipaddon = ZippedAddon(fo)
        prepare_repository(zipaddon, repo, branch)
        pr_no = open_pull_request(repo, branch, zipaddon.id,
                                  zipaddon.version, description)
        post_comment(repo, pr_no, 'Ping @romanvm1972')


if __name__ == '__main__':
    main()
