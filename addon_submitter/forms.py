# coding: utf-8
# Created on: 08.12.2017
# Author: Roman Miroshnychenko aka Roman V.M. (roman1972@gmail.com)

from django.forms import ModelForm
from .models import PullRequest


class PullRequestForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = PullRequest
        fields = ('author',
                  'author_email',
                  'github_username',
                  'addon_description',
                  'git_repo',
                  'git_branch',
                  'zipped_addon',
                  )
