# coding: utf-8
# Created on: 28.11.2017
# Author: Roman Miroshnychenko aka Roman V.M. (roman1972@gmail.com)

import os
from unittest import TestCase, mock

os.environ.setdefault('GH_TOKEN', 'secret_token')
from .github import *


class GitHubTestCase(TestCase):
    def test_execute(self):
        execute(['echo', 'This is test!'])

    def test_create_addon_directory(self):
        mock_zip = mock.MagicMock()
        mock_zip.is_folder = True
        create_addon_directory('/foo/bar', mock_zip)

    @mock.patch('addon_submitter.github.os')
    @mock.patch('addon_submitter.github.execute')
    @mock.patch('addon_submitter.github.shutil')
    def test_prepare_addon_branch(self, *args):
        prepare_pr_branch('repo-plugins', 'krypton', '/foo',
                          'plugin.video.foo', '0.0.1')

    @mock.patch('addon_submitter.github.requests')
    def test_git_hub_api(self, mock_requests):
        mock_resp = mock.MagicMock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {'number': 1}
        mock_requests.post.return_value = mock_resp
        assert open_pull_request('repo-plugins',
                                 'krypton',
                                 'plugin.video.foo',
                                 '0.0.1',
                                 'Cool video plugin') == 1
        post_comment('repo-plugins', 1, 'Hello!')
