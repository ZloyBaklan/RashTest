from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from pycbrf import ExchangeRates
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver


class Item(models.Model):
    CURRENCY_CHOICES = (
            ('RUB', 'rub'),
            ('USD', 'usd'),
        )

    name = models.CharField(
        max_length=200,
        verbose_name='Название товара',
        null=False, unique=True
        )
    description = models.CharField(
        max_length=200,
        verbose_name='Описание товара',
        null=False, help_text='Описание'
        )
    price = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0, 'Значение не может быть меньше 0')],
        verbose_name='Стоимость по умолчанию в рублях',
        )
    currency = models.CharField(
        max_length=3,
        default='RUB',
        verbose_name='Стоимость пересчитается, в $ по курсу ЦБРФ',
        choices=CURRENCY_CHOICES
        )

    class Meta:
        verbose_name = 'Объект платежа'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse("create_session_page", kwargs={"pk": self.pk})

    def get_price(self):
        price = self.price
        currency = self.currency
        today = date.today()
        rates = ExchangeRates(today)
        dollar_curency = rates['USD'].value
        if currency != 'RUB' and currency != 'USD':
            course = rates[currency].value
            # Рассчет кросс курса, через переходной курс доллара из рублей
            pre_price = (price / course)*(course / dollar_curency)
            price = round(pre_price*dollar_curency)
        elif currency == 'USD':
            pass
        else:
            price = ( price / dollar_curency)
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
