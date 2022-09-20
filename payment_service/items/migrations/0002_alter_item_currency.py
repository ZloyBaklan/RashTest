# Generated by Django 4.1.1 on 2022-09-20 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('eur', 'eur'), ('rub', 'rub'), ('usd', 'usd')], default='usd', max_length=3, verbose_name='Валюта'),
        ),
    ]
