# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

import os
from django.conf import settings
from django.test.testcases import TestCase
from ..models import PullRequest


class PullRequestTestCase(TestCase):
    def test_pull_request_model(self):
        path = os.path.join(settings.BASE_DIR, 'test_data',
                            'plugin.video.example-2.2.0.zip')
        with open(path, 'rb') as fo:
            PullRequest.objects.create(
                author='John Doe',
                author_email='jdoe@example.com',
                addon_description='My cool addon',
                git_repo='repo-scripts',
                git_branch='krypton',
                zipped_addon=fo.read()
            )
        pr = PullRequest.objects.all()[0]
        self.assertEqual(str(pr), '[plugin.video.example] 2.2.0')
