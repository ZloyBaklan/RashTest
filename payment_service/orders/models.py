from tkinter import CASCADE
from django.db import models
from django.db.models import Sum
from items.models import Item
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User


#cart = Order.get_cart(request.user)
#Скидки валюты
#оформление заказа

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.user} --- {self.time.ctime()} --- {self.amount}'

class Order(models.Model):
    STATUS_CART = '1_cart'
    STATUS_PAID = '2_paid'
    STATUS_CHOICES = [
        (STATUS_CART, 'cart'),
        (STATUS_PAID, 'paid')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # items = models.ManyToManyField(OrderItem, related_name='orders')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_CART)
    amount = models.IntegerField( blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.user} --- {self.status} --- {self.amount}'
    
    @staticmethod
    def get_cart(user: User):
        cart = Order.objects.filter(user=user, status=Order.STATUS_CART).first()
        if not cart:
            cart = Order.objects.create(user=user,status=Order.STATUS_CART, amount = 0)
        return cart

    def get_amount(self):
        amount = int(0)
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            amount +=item.amount
        return amount
    
    def get_absolute_url(self):
        return reverse("create_session_order_page", kwargs={"pk" : self.pk})

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(null=True)
    discount = models.IntegerField(default=0) 
    '''
    items=[{'price': 'price_CBb6IXqvTLXp3f'}],
    coupon='free-period',

    Альтернатива:
    mode='subscription',
    discounts=[{
          'coupon': '{{COUPON_ID}}',
    }],

    '''

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.product} --- {self.quantity} --- {self.price}'
    
    @property
    def amount(self):
        return self.quantity*(self.price-self.discount)
    
@receiver(post_save, sender=OrderItem)
def recalculate_order_amount_after_save(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()

@receiver(post_delete, sender=OrderItem)
def recalculate_order_amount_after_delete(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Статус %s" % self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'

