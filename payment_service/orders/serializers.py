from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Order

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('owner', 'item')
        model = Order
        validators = [
            UniqueTogetherValidator(
                queryset=Order.objects.all(),
                fields=('owner', 'item'),
                message='Данная позиция уже в заказе'
            )
        ] # можно удалить, чтобы добавлять несколько одинаковых позиций