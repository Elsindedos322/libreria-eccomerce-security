#!/bin/bash
set -e

echo "Starting entrypoint: waiting for DB and running migrations if needed..."

# Try to apply migrations with retries — useful when DB may not be immediately available
MAX_RETRIES=30
COUNT=0
until python manage.py migrate --noinput; do
  COUNT=$((COUNT+1))
  if [ ${COUNT} -ge ${MAX_RETRIES} ]; then
    echo "migrate failed after ${MAX_RETRIES} attempts"
    exit 1
  fi
  echo "Waiting for database... (${COUNT}/${MAX_RETRIES})"
  sleep 2
done

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Entrypoint finished — executing CMD"
exec "$@"
