# Dockerfile for deploying Django app to Cloud Run
FROM python:3.11-slim

# Avoids writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# System deps for psycopg2 and pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    netcat \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better cache
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app/

# Copy entrypoint and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Runtime settings
ENV DJANGO_SETTINGS_MODULE=libreria.libreria.settings
ENV PORT 8080

# Entrypoint will run migrations and collectstatic, then exec the CMD
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "libreria.wsgi:application", "--bind", ":8080", "--workers", "2"]
