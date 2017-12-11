# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

from django.db import models
from .zip_file import ZippedAddon

REPOSITORIES = (
    ('repo-scripts', 'Script addons'),
    ('repo-plugins', 'Content plugins'),
)
BRANCHES = (
    ('leia', '18 Leia'),
    ('krypton', '17 Krypton'),
    ('jarvis', '16 Jarvis'),
    ('isengard', '15 Isengard'),
)


class PullRequest(models.Model):
    """
    Represents a pull request on GitHub for submission an addon
    to the Kodi official repo
    """
    pull_request_number = models.IntegerField('Pull request number',
                                              blank=True, null=True)
    author = models.CharField('Addon author', max_length=200)
    author_email = models.EmailField('Author\'s email')
    addon_source_url = models.URLField('Addon source')
    addon_description = models.TextField('Addon description')
    git_repo = models.CharField('Git repository', max_length=50,
                                choices=REPOSITORIES,
                                default='repo-scripts')
    git_branch = models.CharField('Git branch', max_length=50,
                                  choices=BRANCHES,
                                  default='leia')
    zipped_addon = models.FileField('Zipped addon')
    send_notifications = models.BooleanField('Send notifications', default=True)
    timestamp = models.DateTimeField('Timestamp', auto_now_add=True)

    def get_zipped_addon(self) -> ZippedAddon:
        """
        :return: :class:`ZippedAddon` instance for this pull request
        """
        return ZippedAddon(self.zipped_addon)

    def __str__(self) -> str:
        zipdaddon = self.get_zipped_addon()
        return '{0}-{1}'.format(zipdaddon.id, zipdaddon.version)

    class Meta:
        verbose_name = 'Pull Request'
        verbose_name_plural = 'Pull Requests'
        ordering = ('-pk',)
