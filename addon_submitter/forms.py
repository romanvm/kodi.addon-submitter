# coding: utf-8
# Created on: 08.12.2017
# Author: Roman Miroshnychenko aka Roman V.M. (roman1972@gmail.com)

from zipfile import BadZipFile
from django.forms import ModelForm, ValidationError
from .models import PullRequest
from .zip_file import ZippedAddon


class PullRequestForm(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    def clean(self) -> dict:
        """
        Validate an addon .zip file

        :return: form cleaned data
        """
        cleaned_data = super().clean()
        fo = cleaned_data.get('zipped_addon')
        try:
            ZippedAddon(fo)
        except (BadZipFile, FileNotFoundError, AttributeError):
            self.add_error('zipped_addon',
                           ValidationError(
                               'Bad zip archive or missing addon.xml!'
                           ))
        else:
            fo.seek(0)
        return cleaned_data

    class Meta:
        model = PullRequest
        fields = ('author',
                  'author_email',
                  'addon_source_url',
                  'addon_description',
                  'git_repo',
                  'git_branch',
                  'zipped_addon',
                  )
