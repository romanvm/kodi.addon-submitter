# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'addon_submitter.settings')

app = Celery('addon_submitter')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
