# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.testcases import TestCase
from ..models import PullRequest


class PullRequestTestCase(TestCase):
    def setUp(self):
        self.pull_request = None

    def test_pull_request_model(self):
        filename = 'plugin.video.example-2.2.0.zip'
        path = os.path.join(settings.BASE_DIR, 'test_data', filename)
        fo = open(path, 'rb')
        zipped_addon = SimpleUploadedFile(filename, fo.read(),
                                          'application/zip')
        PullRequest.objects.create(
            author='John Doe',
            author_email='jdoe@example.com',
            addon_description='My cool addon',
            addon_source_url='https://github.com/foo/bar',
            git_repo='repo-scripts',
            git_branch='krypton',
            zipped_addon=zipped_addon
        )
        self.pull_request = PullRequest.objects.all()[0]
        self.assertEqual(str(self.pull_request), 'plugin.video.example-2.2.0')
        print('pull request model test passed')

    def tearDown(self):
        if self.pull_request is not None:
            zip_path = self.pull_request.zipped_addon.path
            if os.path.exists(zip_path):
                self.pull_request.zipped_addon.close()
                os.remove(zip_path)
