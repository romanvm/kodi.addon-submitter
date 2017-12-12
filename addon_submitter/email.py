# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

from smtplib import SMTPException
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_success_message(recipient_name: str,
                         recipient_email: str,
                         addon_id: str,
                         addon_version: str,
                         pull_request_url: str) -> None:
    """
    Send email notification about successful creation of a pull request

    :param recipient_name: addon submitter's name
    :param recipient_email: addon submitter's email
    :param addon_id: addon ID
    :param addon_version: addon version
    :param pull_request_url: the URL of the pull request
    :raises smtplib.SMTPException: on sending failure
    """
    html_mesage = render_to_string(
        'addon_submitter/emails/success.html',
        {
            'name': recipient_name,
            'addon_id': addon_id,
            'addon_version': addon_version,
            'pull_request_url': pull_request_url
        }
    )
    try:
        send_mail(
            subject='Your addon has been accepted',
            message=strip_tags(html_mesage),
            from_email='noreply@example.com',
            recipient_list=[recipient_email],
            html_message=html_mesage
        )
    except SMTPException as ex:
        raise SMTPException('Failed to send email to {name} <{email}>!'.format(
            name=recipient_name,
            email=recipient_email
        )) from ex
