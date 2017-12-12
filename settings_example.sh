#!/usr/bin/env bash
# This is an example of production settings for addon_submitter application.
# Update the options below with your actual values and save the script
# as settings.sh.
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
export EMAIL_USE_SSL="true"
export EMAIL_HOST_USER=""
export EMAIL_HOST_PASSWORD=""
export GH_TOKEN=""
#=== End configuration options ===
