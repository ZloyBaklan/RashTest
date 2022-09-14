from django.contrib import admin
from .models import Order

from django.utils.datetime_safe import datetime

from .models import Order, Entry



class EntryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.order.total += obj.quantity * obj.item.price
        obj.order.count += obj.quantity
        obj.order.updated = datetime.now()
        obj.order.save()
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Order)
admin.site.register(Entry, EntryAdmin)
