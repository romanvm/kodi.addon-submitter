# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

import os
from unittest import TestCase
from django.conf import settings
from ..zip_file import ZippedAddon


class ZippedAddonTestCase(TestCase):
    def test_zipped_addon(self):
        path = os.path.join(settings.BASE_DIR, 'test_data',
                            'plugin.video.example-2.2.0.zip')
        with open(path, 'rb') as fo:
            zip_addon = ZippedAddon(fo)
            self.assertEqual(zip_addon.id, 'plugin.video.example')
            self.assertEqual(zip_addon.version, '2.2.0')
            self.assertTrue(zip_addon.is_folder)
