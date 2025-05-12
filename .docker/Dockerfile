FROM python:3.13.3-slim-bullseye

WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Establecer settings base como default
ENV DJANGO_SETTINGS_MODULE=config.settings.base

# Ejecuta collectstatic + gunicorn al iniciar el contenedor
CMD ["sh", "-c", "python manage.py collectstatic --noinput && newrelic-admin run-program gunicorn config.wsgi:application --bind 0.0.0.0:8080"]
