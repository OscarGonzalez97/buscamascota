# Use the python:3.9-alpine image as the base
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Create and set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Rename a specific settings file to be used
RUN mv buscamascota/local_settings_docker.py buscamascota/local_settings.py

# Run Django migrations
RUN python manage.py migrate

# Create a superuser for the application
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Collect static files
RUN python manage.py collectstatic --no-input

# Start the application using Gunicorn
CMD ["gunicorn", "buscamascota.wsgi:application", "--bind", "0.0.0.0:5000"]
