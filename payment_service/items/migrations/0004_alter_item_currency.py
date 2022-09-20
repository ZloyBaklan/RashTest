# Generated by Django 4.1.1 on 2022-09-20 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_alter_item_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('EUR', 'eur'), ('RUB', 'rub'), ('USD', 'usd')], default='usd', max_length=3, verbose_name='Валюта'),
        ),
    ]
