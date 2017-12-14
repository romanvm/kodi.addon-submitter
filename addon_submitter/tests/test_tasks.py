# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

import os
from collections import namedtuple
from unittest import mock
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.testcases import TestCase
from ..models import PullRequest
from ..tasks import process_submitted_addon

PullRequestResult = namedtuple('PullRequestResult', ['number', 'html_url'])


class TasksTestCase(TestCase):
    # Todo: fix zip file cleanup
    # def setUp(self):
    #     self.pull_request = None

    @mock.patch('addon_submitter.tasks.send_success_message')
    @mock.patch('addon_submitter.tasks.prepare_repository')
    @mock.patch('addon_submitter.tasks.post_comment')
    @mock.patch('addon_submitter.tasks.open_pull_request')
    def test_process_submitted_addon(self, m_open_pr, *args):
        m_open_pr.return_value = PullRequestResult(
            1,
            'https://github.com/jdoe/foo/pulls/1'
        )
        filename = 'plugin.video.example-2.2.0.zip'
        path = os.path.join(settings.BASE_DIR, 'test_data', filename)

        with open(path, 'rb') as fo:
            zipped_addon = SimpleUploadedFile(filename, fo.read(),
                                              'application/zip')
        self.pull_request = PullRequest.objects.create(
            author='John Doe',
            author_email='jdoe@example.com',
            addon_description='My cool addon',
            addon_source_url='https://github.com/foo/bar',
            git_repo='repo-scripts',
            git_branch='krypton',
            zipped_addon=zipped_addon
        )
        process_submitted_addon(self.pull_request.pk)
        m_open_pr.assert_called()

    # def tearDown(self):
    #     if self.pull_request is not None:
    #         zip_path = self.pull_request.zipped_addon.path
    #         if os.path.exists(zip_path):
    #             self.pull_request.zipped_addon.close()
    #             os.remove(zip_path)
