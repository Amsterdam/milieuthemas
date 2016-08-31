#!/usr/bin/env bash

set -u
set -e

cd /app

# collect static files
python manage.py collectstatic --noinput

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini
