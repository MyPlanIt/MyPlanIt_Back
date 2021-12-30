#!/bin/sh

echo "Collect static files"
python manage.py collectstatic --no-input

echo "Apply database migrations"
python manage.py migrate

exec "$@"
