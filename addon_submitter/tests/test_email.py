# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

from unittest import TestCase, mock
from ..email import send_success_message


@mock.patch('addon_submitter.email.send_mail')
class SendEmailTestCase(TestCase):
    def test_send_success_message(self, *args):
        send_success_message(
            recipient_name='John Doe',
            recipient_email='jdoe@example.com',
            addon_id='plugin.video.example',
            addon_version='2.2.0',
            pull_request_url='https://github.com/jdoe/foo/pulls/1'
        )
