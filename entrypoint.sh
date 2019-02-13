#!/bin/sh
# Check production environment variables
if [ -z "$DJANGO_SECRET_KEY" ]; then
    echo >&2 'error: Must specify DJANGO_SECRET_KEY'
    exit 1
fi
if [ "$1" = "gunicorn" ]; then
    ./manage.py migrate
fi
# Start process
exec "$@"