# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from .forms import PullRequestForm
from .tasks import process_submitted_addon
from .models import PullRequest
from .zip_file import ZippedAddon


def index(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PullRequestForm(request.POST, request.FILES)
        if form.is_valid():
            zipped_addon = ZippedAddon(request.FILES['zipped_addon'])
            queryset = PullRequest.objects.filter(
                addon_id=zipped_addon.id,
                addon_version=zipped_addon.version
            )
            if queryset.exists():
                pull_request = queryset[0]
                pull_request.zipped_addon = request.FILES['zipped_addon']
                pull_request.save()
            else:
                pull_request = form.save()
            # Add the pull request to Celery task queue
            process_submitted_addon.delay(pull_request.pk)
            return HttpResponseRedirect(reverse('confirmation'))
    else:
        form = PullRequestForm()
    return render(request, 'addon_submitter/index.html', {'form': form})


def confirmation(request: HttpRequest) -> HttpResponse:
    return render(request, 'addon_submitter/confirmation.html')
