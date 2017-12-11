# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_success_message(recipient_name: str,
                         recipient_email: str,
                         addon_id: str,
                         addon_version: str,
                         pull_request_url: str) -> None:
    pass
