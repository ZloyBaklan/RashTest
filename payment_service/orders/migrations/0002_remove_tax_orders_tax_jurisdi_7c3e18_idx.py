# Generated by Django 4.1.1 on 2022-09-19 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='tax',
            name='orders_tax_jurisdi_7c3e18_idx',
        ),
    ]
