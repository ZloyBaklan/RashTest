from django.shortcuts import render
from django.http import HttpResponse
from .models import Order, Entry
from items.models import Item
from django.contrib.auth.models import User
import stripe
import json
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.core.paginator import Paginator

from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY

def test_view(request):
    """ This view displays what is in a user's cart. """
    # Based on the user who is making the request, grab the cart object
    my_order = Order.objects.get_or_create(owner=User)
    # Get a queryset of entries that correspond to "my_cart"
    list_of_entries = Entry.objects.filter(order=my_order)
    
    items = Item.objects.all()

    if request.POST:
        # Get the product's ID from the POST request.
        item_id = request.POST.get('item_id')
        # Get the object using our unique primary key
        item_obj = Item.objects.get(id=item_id)
        # Get the quantity of the product desired.
        item_quantity = request.POST.get('item_quantity')
        # Create the new Entry...this will update the cart on creation
        Entry.objects.create(cart=my_order, item=item_obj, quantity=item_quantity)
        return HttpResponse('mainpage.html')

    return render(request, 'mainpage.html', {'my_order': my_order, 'list_of_entries': list_of_entries,
                                              'items': items})

class Order_Page_View(TemplateView):
    template_name = "mainpage.html"

    def get_context_data(self, **kwargs):
        order = Order.objects.get(id=self.kwargs['pk'])
        context = super(Order_Page_View, self).get_context_data(**kwargs)
        context.update({
            "product": order,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context

class Create_Checkout_Session_Order_View(View):
    def get(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = Order.objects.get(id=order_id)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': order.total,
                        'product_data': {
                            'name': f'Заказ № {order_id}',
                            'description': f'Единиц товара: {order.count}',
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