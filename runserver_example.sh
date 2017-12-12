#!/usr/bin/env bash
# This is an example of a script that runs addon_submitter application
# in a production environment.
# Update the options below with your actual values and save the script
# as runserver.sh.
# All option values must be provided!

#===== Configuration options =====
export DJANGO_SETTINGS_MODULE="addon_submitter.settings_prod"
# Use a unique secret key in production!
export SECRET_KEY="some_long_random_string"
export ALLOWED_HOSTS="addon-submitter.duckdns.org"
export DB_ENGINE="django.db.backends.postgresql_psycopg2"
export DB_NAME="addon_submitter"
export DB_USER="addon_submitter"
export DB_PASS="1111" # Use a strong password!
export PROXY_USER="romanvm1972"
export USER_NAME="Roman Miroshnychenko"
export USER_EMAIL="roman1972@gmail.com"
export UPSTREAM_USER="romanvm"
export EMAIL_HOST="smtp.ukr.net"
export EMAIL_PORT="465"
export EMAIL_HOST_USER=""
export EMAIL_HOST_PASSWORD=""
export GH_TOKEN=""
#=== End configuration options ===

SOCKET=$HOME/kodi.addon-submitter/addon-submitter.sock

cd $HOME/kodi.addon-submitter
pipenv run gunicorn --workers 3 --bind $SOCKET addon_submitter.wsgi:application
