# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

import os
from io import BytesIO
from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase, mock
from ..models import PullRequest


class IndexViewTestCase(TestCase):
    def test_index_view_get(self):
        resp = self.client.get(reverse('index'))
        self.assertContains(resp, 'Submit Kodi Addon')

    @mock.patch('addon_submitter.views.process_submitted_addon')
    def test_index_view_post_valid(self, *args):
        zip_path = os.path.join(settings.BASE_DIR, 'test_data',
                                'plugin.video.example-2.2.0.zip')
        with open(zip_path, 'rb') as fo:
            data = {
                'author': 'John Doe',
                'author_email': 'jdoe@example.com',
                'addon_source_url': 'https://github.com/jdoe/foo',
                'addon_description': 'My cool addon',
                'git_repo': 'repo-plugins',
                'git_branch': 'leia',
                'zipped_addon': fo,
            }
            resp = self.client.post(reverse('index'), data)
            self.assertRedirects(resp, reverse('confirmation'))
            pull_request1 = PullRequest.objects.get(
                addon_id = 'plugin.video.example',
                addon_version = '2.2.0'
            )
            self.client.post(reverse('index'), data)
            pull_request2 = PullRequest.objects.get(
                addon_id='plugin.video.example',
                addon_version='2.2.0'
            )
            self.assertEqual(pull_request2.pk, pull_request1.pk)
            if os.path.exists(pull_request1.zipped_addon.path):
                pull_request1.zipped_addon.close()
                os.remove(pull_request1.zipped_addon.path)

    def test_index_view_post_invalid_zip(self):
        data = {
            'author': 'John Doe',
            'author_email': 'jdoe@example.com',
            'addon_source_url': 'https://github.com/jdoe/foo',
            'addon_description': 'My cool addon',
            'git_repo': 'repo-plugins',
            'git_branch': 'leia',
            'zipped_addon': BytesIO(b'foobar'),
        }
        resp = self.client.post(reverse('index'), data)
        self.assertTrue(resp.context['form'].errors)


class ConfirmationViewTestCase(TestCase):
    def test_confirmation_view(self):
        resp = self.client.get(reverse('confirmation'))
        self.assertContains(resp, 'Addon Has Been Submitted')
