# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

# Install dependencies including ODBC driver for SQL Server
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    gnupg \
    unixodbc-dev \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Copy manage.sh present at repo root (compose build context is ..)
COPY manage.sh /app/manage.sh
COPY send_task.py /app/send_task.py
COPY celery_app.py tasks.py celery_config.py /app/
COPY app /app/app

# Normalize CRLF and make it executable
RUN sed -i 's/\r$//' /app/manage.sh && chmod +x /app/manage.sh

# Optional: install Python deps if you have a requirements file
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# No CMD here; docker-compose sets: command: ./manage.sh