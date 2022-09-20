# Generated by Django 4.1.1 on 2022-09-20 09:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
                ('description', models.CharField(help_text='Описание', max_length=200, verbose_name='Описание')),
                ('price', models.PositiveSmallIntegerField(default=0, help_text='В центах, на сайте в $', validators=[django.core.validators.MinValueValidator(0, 'Значение не может быть меньше 0')], verbose_name='Стоимость')),
                ('currency', models.CharField(choices=[('eur', 'EUR'), ('rub', 'RUB'), ('usd', 'USD')], default='usd', max_length=3, verbose_name='Валюта')),
            ],
            options={
                'verbose_name': 'Объект платежа',
                'ordering': ['name'],
            },
        ),
    ]
