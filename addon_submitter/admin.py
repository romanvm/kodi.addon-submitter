# coding: utf-8
# Created on: 08.12.2017
# Author: Roman Miroshnychenko aka Roman V.M. (roman1972@gmail.com)

from django.contrib import admin
from .models import PullRequest


@admin.register(PullRequest)
class PullRequestAdmin(admin.ModelAdmin):
    list_display = ('author', 'author_email', 'git_repo', 'git_branch',
                    'timestamp')
    search_fields = ('author', 'author_email')
    ordering = ('-pk',)
