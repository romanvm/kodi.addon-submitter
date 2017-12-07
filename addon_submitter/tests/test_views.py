# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

from django.shortcuts import reverse
from django.test import TestCase


class IndexViewTestCase(TestCase):
    def test_index_view(self):
        resp = self.client.get(reverse('index'))
        self.assertContains(resp, 'Submit Kodi Addon')
