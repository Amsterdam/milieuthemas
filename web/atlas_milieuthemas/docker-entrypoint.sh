#!/usr/bin/env bash

set -u
set -e

cd /app

# collect static files
python manage.py collectstatic --noinput

# migrate database tables
yes yes | python manage.py migrate --noinput

# run import
python manage.py run_import

# sync geo views
python manage.py sync_views

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini
