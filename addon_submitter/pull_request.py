# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com
"""Functions for working with GitHub pull requests"""

import os
import logging
import shutil
import subprocess
from django.conf import settings
from addon_submitter.zip_file import ZippedAddon

REPO_URL_MASK = 'https://{gh_token}@github.com/{user}/{repo}.git'
GH_TOKEN = os.environ['GH_TOKEN']

logger = logging.getLogger(__name__)
if settings.DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO
logger.setLevel(level)


def execute(args: list) -> None:
    """
    Execute a console command

    :param args: command with arguments
    :raises RuntimeError: if command returns non-0 code
    """
    call_string = ' '.join(args)
    logging.debug('Executing: ' + call_string)
    res = subprocess.call(args)
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


def prepare_pull_request(zipaddon: ZippedAddon, repo: str, branch: str) -> None:
    workdir = settings.WORKDIR
    try:
        create_addon_directory(workdir, zipaddon)
        prepare_pr_branch(repo, branch, workdir, zipaddon.id, zipaddon.version)
    except Exception:
        logging.exception('Error while preparing pull request!')
    finally:
        # shutil.rmtree(os.path.join(workdir, repo), ignore_errors=True)
        shutil.rmtree(os.path.join(workdir, zipaddon.id), ignore_errors=True)


def main():
    import sys
    sys.path.append(settings.BASE_DIR)
    repo = 'repo-scripts'
    branch = 'krypton'
    addon = 'plugin.video.example-2.2.0.zip'
    with open(os.path.join(settings.BASE_DIR,
                           'test_data', addon), 'rb') as fo:
        prepare_pull_request(ZippedAddon(fo), repo, branch)


if __name__ == '__main__':
    main()
