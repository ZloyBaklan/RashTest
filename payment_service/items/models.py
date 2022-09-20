from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from pycbrf import ExchangeRates
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver


class Item(models.Model):
    CURRENCY_CHOICES = (
            ('RUB','rub'),
            ('USD','usd'),
        )
    
    name = models.CharField(max_length=200, verbose_name='Название',
                            null=False, unique=True)
    description = models.CharField(max_length=200, verbose_name='Описание',
                                   null=False, help_text='Описание')
    price = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0, 'Значение не может быть меньше 0')],
        verbose_name='Стоимость', help_text='На сайте оплаты в $'
    )
    currency = models.CharField(max_length=3, default='usd', verbose_name='Валюта',
                                choices=CURRENCY_CHOICES)


    class Meta:
        verbose_name = 'Объект платежа'
        ordering = ['name']


    def get_absolute_url(self):
        return reverse("create_session_page", kwargs={"pk" : self.pk})

    
    def get_price(self):
        price = self.price
        currency = self.currency
        today = date.today()
        rates = ExchangeRates(today)
        course = rates[currency].value
        if currency != 'RUB':
            price = round(price / course)
        else:
            pass
        return int(price)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Item)
def recalculate_item_price_after_save(sender, instance, **kwargs):
    item = instance
    item.price = item.get_price()
    post_save.disconnect(recalculate_item_price_after_save, sender)
    item.save()
    post_save.connect(recalculate_item_price_after_save, sender)
