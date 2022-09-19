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
    STATUS_WAITING_FOR_PAYMENT = '2_waiting_for_payment'
    STATUS_PAID = '3_paid'
    STATUS_CHOICES = [
        (STATUS_WAITING_FOR_PAYMENT, 'waiting_for_payment'),
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
    
    def make_order(self):
        items = self.orderitem_set.all()
        if items and self.status == Order.STATUS_CART:
            self.status = Order.STATUS_WAITING_FOR_PAYMENT
            self.save()
    
    @staticmethod
    def get_amount_of_unpaid_orders(user: User):
        amount = Order.objects.filter(user=user, status=Order.STATUS_WAITING_FOR_PAYMENT).aggregate(Sum('amount'))['amount__sum']
        return amount or int(0)
    
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

'''
class Order(models.Model):
    user = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#total price for all products in order
    customer_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Заказ %s %s" % (self.pk, self.status.name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):

        super(Order, self).save(*args, **kwargs)


class Order(models.Model):
    # You can change as a Foreign Key to the user model
    customer_email = models.EmailField(
        verbose_name='Customer Email'
    )

    item = models.ForeignKey(
        to=Item,
        verbose_name='Item',
        on_delete=models.PROTECT
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    stripe_payment_intent = models.CharField(
        max_length=200, null=True
    )

    # This field can be changed as status
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return self.customer_email


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.PROTECT)
    product = models.ForeignKey(Item, blank=True, null=True, default=None, on_delete=models.PROTECT)
    nmb = models.IntegerField(default=1)
    price_per_item = models.PositiveSmallIntegerField(default=0)
    total_price = models.PositiveSmallIntegerField(default=0)#price*nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'


    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)


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
'''