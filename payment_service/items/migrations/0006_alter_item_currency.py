# Generated by Django 4.1.1 on 2022-09-20 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_alter_item_currency_alter_item_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('RUB', 'rub'), ('USD', 'usd')], default='RUB', max_length=3, verbose_name='Стоимость пересчитается, в $ по курсу ЦБРФ'),
        ),
    ]
