# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com
"""Functions for working with GitHub pull requests"""

import os
import shutil
from django.conf import settings
from .zip_file import ZippedAddon

REPO_URL_MASK = 'https://{gh_token}@github.com/{user}/{repo}.git'


def create_addon_directory(workdir: str, zipaddon: ZippedAddon) -> str:
    """
    Create a directory for addon

    :param workdir: working directory
    :param zipaddon: zipped addon
    :return: addon directory
    """
    if not zipaddon.is_folder:
        os.chdir(workdir)
        addon_dir = os.path.join(workdir, zipaddon.id)
        os.mkdir(addon_dir)
    else:
        addon_dir = workdir
    zipaddon.extract(addon_dir)
    return addon_dir


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
        gh_token=os.environ['GH_TOKEN'],
        user= settings.PROXY_USER,
        repo=repo
    )
    os.system('git clone {0}'.format(repo_url))
    os.chdir(repo)
    os.system('git config user.name {0}'.format(settings.USER_NAME))
    os.system('git config user.email {0}'.format(settings.USER_EMAIL))
    os.system(
        'git remote add upstream https://github.com/{user}/{repo}.git'.format(
        user=settings.UPSTREAM_USER,
        repo=repo
    ))
    os.system('git fetch upstrem')
    os.system('git checkout -b {0} --track origin/{0}'.format(branch))
    os.system('git merge upstream/{0}'.format(branch))
    os.system('git branch -D {0}'.format(addon_id))
    os.system('git checkout -b {0}'.format(addon_id))
    shutil.rmtree(os.path.join(workdir, repo, addon_id), ignore_errors=True)
    shutil.copytree(os.path.join(workdir, addon_id),
                    os.path.join(workdir, repo, addon_id))
    os.system('git add --all .')
    os.system('git commit -m "[{id}] {version}"'.format(
        id=addon_id,
        version=addon_version))
    os.system('git push --force --quiet origin {0}'.format(addon_id))
