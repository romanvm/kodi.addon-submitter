# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'addon_submitter/index.html')
