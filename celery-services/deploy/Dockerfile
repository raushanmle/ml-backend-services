# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

# Optional: if your script uses bash
RUN apt-get update && apt-get install -y --no-install-recommends bash ca-certificates \
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