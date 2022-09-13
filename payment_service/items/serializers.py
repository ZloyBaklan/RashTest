from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('__all__')
        lookup_field = 'id'
        extra_kwargs = {'url': {'lookup_field': 'id'}}