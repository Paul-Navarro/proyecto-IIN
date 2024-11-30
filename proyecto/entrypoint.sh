#!/bin/bash

echo "Waiting for Postgres to start..."
sleep 10
echo "Postgres is up and running"

echo "Migrating database..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput



gunicorn proyecto.wsgi:application --bind 0.0.0.0:8000 --workers 3