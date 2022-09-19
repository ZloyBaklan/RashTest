from items.models import Item
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import stripe
import json
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.generic import DeleteView, ListView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from .forms import AddQuantityForm
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url=reverse_lazy('home'))
def add_item_to_cart(request, pk):
    if request.method == 'POST':
        quantity_form = AddQuantityForm(request.POST)
        if quantity_form.is_valid():
            quantity = quantity_form.cleaned_data['quantity']
            customer = User.objects.get(id=request.user.pk)
            if quantity:
                cart = Order.get_cart(customer)
                # product = Product.objects.get(pk=pk)
                product = get_object_or_404(Item, pk=pk)
                cart.orderitem_set.create(product=product,
                                          quantity=quantity,
                                          price=product.price)
                cart.save()
                return redirect('cart_view')
            else:
                pass
    return redirect('home')


@login_required(login_url=reverse_lazy('home'))
def cart_view(request):
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    email = request.user.email
    context = {
        'cart': cart,
        'email': email,
        'items': items,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'cart.html', context)

@method_decorator(login_required, name='dispatch')
class CartDeleteItem(DeleteView):
    model = OrderItem
    template_name = 'cart.html'
    success_url = reverse_lazy('cart_view')

    # Проверка доступа
    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(order__user=self.request.user)
        return qs



class OrderHistoryListView(ListView):
    model = Order
    template_name = "order_history.html"


class Order_Page_View(TemplateView):
    template_name = "mainpage.html"

    def get_context_data(self, **kwargs):
        order = Order.objects.get(id=self.kwargs['pk'])
        context = super(Order_Page_View, self).get_context_data(**kwargs)
        email = order.user.email
        context.update({
            "order": order,
            'email': email,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class Create_Checkout_Session_Order_View(View):
    def get(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = Order.objects.get(id=order_id)
        checkout_session = stripe.checkout.Session.create(
            customer_email = order.user.email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': order.amount,
                        'product_data': {
                            'name': f'Заказ № {order_id}',
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


'''

stripe.PaymentIntent.create(
  amount=1099,
  currency='usd',
  # automatic_payment_methods={"enabled": True},
  payment_method_types=['card'],
  metadata={
    'order_id': '6735',
  },
)

'''



'''
def checkout(request):
    if request.user.is_authenticated:
        cart = Profile.objects.get(user= request.user).cart
        total = cart.aggregate(Sum('price'))['price__sum']
        return render(request,"checkout.html", {"cart":cart, "total":total})
    else:
        redirect('home')


class PaymentSuccessView(TemplateView):
    template_name = "success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return 'cancel.html'
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(Order, stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)

'''



'''
@csrf_exempt
def createpayment(request):
    if request.user.is_authenticated:
        cart = Profile.objects.get(user=request.user).items
        total = cart.aggregate(Sum('price'))['price_sum']
        total = total*100
        if request.method=='POST':
            data = json.loads(request.body)
            intent = stripe.PaymentIntent.create(
            amount=total,
            currency=data['currency'],
            metadata={'integration_check': 'accept_a_payment'},
            )
            try:
               return JsonResponse({'publishableKey':  
                    settings.STRIPE_PUBLIC_KEY, 'clientSecret': intent.client_secret})
            except Exception as e:
                return JsonResponse({'error':str(e)},status= 403)
'''

'''
def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, defaults={"nmb": nmb})
        if not created:
            print ("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    #common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in  products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)
'''

'''
def test_view(request):
    """ This view displays what is in a user's cart. """
    # Based on the user who is making the request, grab the cart object
    owner = User.objects.filter(email='39359760@yandex.ru')
    my_order = Order.objects.get_or_create(owner=owner)
    # Get a queryset of entries that correspond to "my_cart"
    list_of_entries = Entry.objects.filter(order=2)
    print(owner)
    print(my_order)
    print(list_of_entries)
    items = Item.objects.all()
    print(items)

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

    return render(request, 'index.html', {'my_order': my_order, 'list_of_entries': list_of_entries,
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
'''