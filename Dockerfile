# Use official Python image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
# Copy project files
COPY . /app/

# Collect static files (if you're deploying)
# RUN python manage.py collectstatic --noinput

# Run development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "migrate"]
