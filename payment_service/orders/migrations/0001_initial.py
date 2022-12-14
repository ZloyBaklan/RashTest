# Generated by Django 4.1.1 on 2022-09-20 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent_off', models.IntegerField()),
                ('duration', models.CharField(choices=[('forever', 'forever'), ('once', 'once'), ('repeating', 'repeating')], max_length=9)),
                ('duration_in_months', models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1_cart', 'cart'), ('2_paid', 'paid')], default='1_cart', max_length=32)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('jurisdiction', models.CharField(default='RU', max_length=2)),
                ('discount', models.ManyToManyField(blank=True, to='orders.discount')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_id', models.CharField(max_length=255)),
                ('display_name', models.CharField(default='vat', max_length=10)),
                ('jurisdiction', models.CharField(choices=[('US', 'US'), ('RU', 'RU')], max_length=2)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('inclusive', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.discount')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.IntegerField(null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='items.item')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.tax'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
