# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from .forms import PullRequestForm


def index(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PullRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('confirmation'))
    else:
        form = PullRequestForm()
    return render(request, 'addon_submitter/index.html', {'form': form})


def confirmation(request: HttpRequest) -> HttpResponse:
    return render(request, 'addon_submitter/confirmation.html')
