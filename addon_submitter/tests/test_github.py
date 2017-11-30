# coding: utf-8
# Created on: 28.11.2017
# Author: Roman Miroshnychenko aka Roman V.M. (roman1972@gmail.com)

import os
from unittest import TestCase, mock

os.environ.setdefault('GH_TOKEN', 'secret_token')
from ..github import *


class GitHubTestCase(TestCase):
    @mock.patch('addon_submitter.github.os')
    @mock.patch('addon_submitter.github.shutil')
    @mock.patch('addon_submitter.github.subprocess')
    def test_prepare_repository(self, m_subpr, *args):
        m_subpr.call.return_value = 0
        mock_zipaddon = mock.MagicMock()
        mock_zipaddon.id = 'plugin.video.foo'
        mock_zipaddon.version = '0.0.1'
        mock_zipaddon.is_folder = True
        prepare_repository(mock_zipaddon, 'repo-plugins', 'krypton')

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
