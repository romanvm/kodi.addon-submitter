# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

import logging
from celery import shared_task
from .models import PullRequest
from .github import prepare_repository, open_pull_request
from .email import send_success_message


@shared_task
def process_submitted_addon(pk: int, new_submission: bool) -> None:
    """
    Process submitted addon asynchronously with Celery

    :param pk: primary key for PullRequest model instance
    :param new_submission: ``True`` for newly submitted addon
    """
    pull_request = PullRequest.objects.get(pk=pk)
    logging.debug('Processing addon {0}'.format(pull_request))
    try:
        zipped_addon = pull_request.get_zipped_addon()
        prepare_repository(
            zipped_addon,
            pull_request.git_repo,
            pull_request.git_branch
        )
        if new_submission:
            result = open_pull_request(
                pull_request.git_repo,
                pull_request.git_branch,
                zipped_addon.id,
                zipped_addon.version,
                pull_request.addon_description
            )
            logging.debug('Pull request created: {0}'.format(result))
            pull_request.pull_request_number = result.number
            pull_request.pull_request_url = result.html_url
            pull_request.save()
            html_url = result.html_url
        else:
            html_url = pull_request.pull_request_url
        send_success_message(
            pull_request.author,
            pull_request.author_email,
            zipped_addon.id,
            zipped_addon.version,
            html_url
        )
        logging.debug('Confirmation mail for {0} sent.'.format(pull_request))
    except Exception:
        logging.exception(
            'Error while processing a submitted addon {0}!'.format(pull_request)
        )
