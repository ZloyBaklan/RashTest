import stripe
import json
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy

from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY

class ItemCreateView(CreateView):
    model = Item
    fields = '__all__'
    template_name = "item_create.html"
    success_url = reverse_lazy("home")

class ItemListView(ListView):
    model = Item
    template_name = "items_list.html"
    context_object_name = 'items_list'

class Item_Page_View(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        item = Item.objects.get(id=self.kwargs['pk'])
        context = super(Item_Page_View, self).get_context_data(**kwargs)
        context.update({
            "product": item,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context

class Create_Checkout_Session_Item_View(View):
    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['pk']
        item = Item.objects.get(id=item_id)
        checkout_session = stripe.checkout.Session.create(
            client_reference_id = request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': item.currency,
                        'exchange_rate': 3,
                        'unit_amount': item.amount,
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/orders/success/',
            cancel_url='http://127.0.0.1:8000/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def create_checkout_session(request, pk):

    request_data = json.loads(request.body)
    item = get_object_or_404(Item, pk=pk)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request_data['email'],
        payment_method_types=['card'],
        allow_promotion_codes = True,
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancel/',
    )
    return JsonResponse({'sessionId': checkout_session.id})

class Success_View(TemplateView):
    template_name = "success.html"


class Cancel_View(TemplateView):
    template_name = "cancel.html"
