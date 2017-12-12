#!/usr/bin/env bash
# This script is used to run addon_submitter application
# in a production environment.

SOCKET=http://unix:$HOME/kodi.addon-submitter/addon-submitter.sock

cd $HOME/kodi.addon-submitter
source settings.sh
pipenv run gunicorn --workers 3 --bind $SOCKET addon_submitter.wsgi:application
