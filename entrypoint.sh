#!/bin/bash
set -e

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c '\q'; do
  echo "Postgres is unavailable - waiting..."
  sleep 2
done

echo "Running database migrations..."
flask --app run db upgrade

echo "Starting Gunicorn..."
exec gunicorn -w 4 -b 0.0.0.0:5000 run:app
