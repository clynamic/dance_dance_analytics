#!/bin/bash
set -e

POSTGRES_USER=${DATABASE_URL#*://}
POSTGRES_USER=${POSTGRES_USER%%:*}

POSTGRES_PASSWORD=${DATABASE_URL#*://${POSTGRES_USER}:}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD%%@*}

POSTGRES_HOSTPORT=${DATABASE_URL#*@}
POSTGRES_HOST=${POSTGRES_HOSTPORT%%/*}
POSTGRES_PORT=${POSTGRES_HOST#*:}
POSTGRES_HOST=${POSTGRES_HOST%%:*}

MAX_WAIT=60
WAIT_INTERVAL=2
elapsed=0

echo "Waiting for Postgres to be available at $POSTGRES_USER:*****@$POSTGRES_HOST:$POSTGRES_PORT"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -p "${POSTGRES_PORT:-5432}" -c '\q' >/dev/null 2>&1; do
  [ $elapsed -ge $MAX_WAIT ] && echo "Postgres is unavailable. Exiting." && exit 1
  sleep $WAIT_INTERVAL
  elapsed=$((elapsed + WAIT_INTERVAL))
done

flask --app run db upgrade
exec gunicorn -w 4 -b 0.0.0.0:5000 run:app
