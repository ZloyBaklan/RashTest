from django.db import models
from django.db.models import Sum
from items.models import Item
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.datetime_safe import datetime


User = get_user_model()



class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="Владелец заказа",
                               related_name="owner")
    count = models.PositiveIntegerField(default=0)
    total = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Заказ'

    def __str__(self):
        return "User: {} has {} items in their order. Their total is ${}".format(self.owner, self.count, self.total)
    
    def total_price(self):
          return Order.objects.aggregate(Sum('item'))

    def get_absolute_url(self):
        return reverse("create_session_order_page", kwargs={"pk" : self.pk})

class Entry(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "This entry contains {} {}(s).".format(self.quantity, self.item.name)

@receiver(post_save, sender=Entry)
def update_order(sender, instance, **kwargs):
    line_cost = instance.quantity * instance.item.price
    instance.order.total += line_cost
    instance.order.count += instance.quantity
    instance.order.updated = datetime.now()

