import stripe
import json
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView

from .models import Item
from .serializers import ItemSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class Item_Page_View(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        item = Item.objects.get(name='Test')
        context = super(Item_Page_View, self).get_context_data(**kwargs)
        context.update({
            "product": item,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context

class Create_Checkout_Session_Item_View(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs['pk']
        item = Item.objects.get(id=item_id)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/cancel/',
        )

        return JsonResponse({
            'id': checkout_session.id
        })


class Success_View(TemplateView):
    template_name = "success.html"


class Cancel_View(TemplateView):
    template_name = "cancel.html"

