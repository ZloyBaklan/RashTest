from django.contrib import admin


from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'price'
    )
    empty_value_display = '-пусто-'


admin.site.register(Item, ItemAdmin)
