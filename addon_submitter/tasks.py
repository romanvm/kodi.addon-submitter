# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

from celery import shared_task
from .models import PullRequest
from .github import prepare_repository, open_pull_request, post_comment


@shared_task
def process_submitted_addon(pk: int) -> None:
    """
    Process submitted addon asynchronously with Celery

    :param pk: primary key for PullRequest model instance
    """
    pass
