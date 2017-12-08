# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

from .settings import *
from django.core.exceptions import ImproperlyConfigured

try:
    DEBUG = bool(os.environ.get('DEBUG'))
    SECRET_KEY = os.environ['SECRET_KEY']
    # Allowed hosts are set as a comma-separated list, eg:
    # export ALLOWED_HOSTS="foo.com,bar.org,baz.net"
    ALLOWED_HOSTS += os.environ['ALLOWED_HOSTS'].split(',')
except KeyError as ex:
    raise ImproperlyConfigured(
        'Variable for production environments is not set!'
    ) from ex
