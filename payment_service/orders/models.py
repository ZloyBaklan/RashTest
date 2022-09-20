from django.db import models
from items.models import Item
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User



class Discount(models.Model):
    DURATION = (
        ('forever', 'forever'),
        ('once', 'once'),
        ('repeating', 'repeating')
    )
    percent_off = models.IntegerField()
    duration = models.CharField(choices=DURATION, max_length=9)
    duration_in_months = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return f"{self.percent_off}%"


class Tax(models.Model):
    JURISDICTION = (
        ('US', 'US'),
        ('RU', 'RU')
    )

    tax_id = models.CharField(max_length=255)
    display_name = models.CharField(default='vat', max_length=10)
    jurisdiction = models.CharField(choices=JURISDICTION, max_length=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    inclusive = models.BooleanField()

    def __str__(self):
        return f"{self.jurisdiction} - {self.percentage}%"
    


class Order(models.Model):
    STATUS_CART = '1_cart'
    STATUS_PAID = '2_paid'
    STATUS_CHOICES = [
        (STATUS_CART, 'cart'),
        (STATUS_PAID, 'paid')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_CART)
    amount = models.IntegerField( blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, blank=True, null=True)
    discount = models.ManyToManyField(Discount, blank=True)
    jurisdiction = models.CharField(max_length=2, default='RU')
    
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

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.product} --- {self.quantity} --- {self.price}'
    
    @property
    def amount(self):
        return self.quantity*(self.price)
    
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


class PromoCode(models.Model):
    code = models.CharField(max_length=255, unique=True)
    coupon = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code}"
