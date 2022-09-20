#!/bin/sh
cd payment_service/
# Запускаем миграции, загружаем фикстуры, собираем и сжимаем статику
python manage.py makemigrations

echo "Making migrations."
python manage.py migrate

# echo "Compressing static files."
# python manage.py compress

# Запускаем gunicorn на нашем $PORT
# echo "Starting gunicorn"
# gunicorn api.wsgi:application --bind 0.0.0.0:8000 \

exec "$@"