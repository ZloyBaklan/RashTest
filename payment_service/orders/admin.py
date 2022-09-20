from django.contrib import admin

from .models import Order, OrderItem, Discount, Tax, PromoCode


admin.site.register(Order)
admin.site.register(PromoCode)
admin.site.register(Tax)
admin.site.register(Discount)
admin.site.register(OrderItem)
