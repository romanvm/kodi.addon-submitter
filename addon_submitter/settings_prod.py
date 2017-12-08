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
    DATABASES = {
        'default': {
            'ENGINE': os.environ['DB_ENGINE'],
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    PROXY_USER = os.environ['PROXY_USER']
    USER_NAME = os.environ['USER_NAME']
    USER_EMAIL = os.environ['USER_EMAIL']
    UPSTREAM_USER = os.environ['UPSTREAM_USER']
except KeyError as ex:
    raise ImproperlyConfigured(
        'Variable for the production environments is not set!'
    ) from ex
