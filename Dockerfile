# Создать образ на основе базового слоя python (там будет ОС и интерпретатор Python).
# 3.7 — используемая версия Python.
# slim — обозначение того, что образ имеет только необходимые компоненты для запуска,
# он не будет занимать много места при развёртывании.
FROM python:3.7-slim

WORKDIR /code 

COPY . .

RUN pip install --upgrade pip && pip install -r /code/requirements.txt

# Выполнить запуск сервера разработки при старте контейнера.
CMD python manage.py makemigrations items && \
    python manage.py makemigrations orders && \
    python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000

ENV DJANGO_SECRET_KEY 'django-insecure--4!$a4k3a5riquz(vam8+*l378^#3kvunyvo5=-hg&7c!s7kf('
ENV DEBUG False