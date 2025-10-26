# Multi-stage Dockerfile: builder, django_test_stage (CI tests), production

############################
# Stage: builder
############################
FROM python:3.11-slim as builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# System deps for psycopg2 and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

############################
# Stage: django_test_stage (used by CI to run tests)
############################
FROM builder as django_test_stage
WORKDIR /app
COPY . /app/

# Note: tests will be executed by CI by running this image and invoking manage.py test

############################
# Stage: production
############################
FROM builder as production
WORKDIR /app
COPY . /app/

# Copy and make entrypoint executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Collect static (may be non-fatal if assets require node tooling)
ENV DJANGO_SETTINGS_MODULE=libreria.libreria.settings
RUN python manage.py collectstatic --noinput || echo "collectstatic failed (build may require node/tailwind)"

ENV PORT 8080
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "libreria.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4"]
