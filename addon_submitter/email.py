# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_success_message(recipient_name: str,
                         recipient_email: str,
                         addon_id: str,
                         addon_version: str,
                         pull_request_url: str) -> None:
    html_mesage = render_to_string(
        'addon_submitter/emalis/success.html',
        {
            'name': recipient_name,
            'addon_id': addon_id,
            'addon_version': addon_version,
            'pull_request_url': pull_request_url
         }
    )
    res = send_mail(
        subject='Your addon has been accepted',
        message=strip_tags(html_mesage),
        from_email='noreply@example.com',
        recipient_list=[recipient_email],
        html_message=html_mesage
    )
    if not res:
        logging.error('Failed to send email to {name} <{email}>!'.format(
            name=recipient_name,
            email=recipient_email
        ))
