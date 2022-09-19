from django.contrib import admin
from .models import Order

from django.utils.datetime_safe import datetime

from .models import Order, Payment, OrderItem


admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderItem)

