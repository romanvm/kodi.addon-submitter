# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com
"""Functions for working with GitHub pull requests"""

import os
from .zip_file import ZippedAddon

REPO_URL_MASK = 'https://{gh_token}@github.com/{repo_slug}.git'


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
