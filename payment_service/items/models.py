from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название',
                            null=False, unique=True)
    description = models.CharField(max_length=200, verbose_name='Описание',
                                   null=False, help_text='Описание')
    price = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0, 'Значение не может быть меньше 0')],
        verbose_name='Стоимость', help_text='В центах, на сайте в $'
    )


    class Meta:
        verbose_name = 'Объект платежа'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("create_session_page", kwargs={"pk" : self.pk})

    '''
    price = models.CharField(max_length=7, default=0,
                             verbose_name='Стоимость')
    '''