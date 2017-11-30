# coding: utf-8
# Created on: 30.11.2017
# Author: Roman Miroshnychenko aka Roman V.M. (roman1972@gmail.com)
"""Production settings"""

from .settings import *

DEBUG = not os.environ.get('DEBUG')
SECRET_KEY = os.environ['SECRET_KEY']
