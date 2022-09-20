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
from .models import Order, OrderItem, Tax, Discount, PromoCode
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
    for tax in Tax.objects.all():
                new_tax = stripe.TaxRate.create(
                    display_name=tax.display_name,
                    jurisdiction=tax.jurisdiction,
                    percentage=tax.percentage,
                    inclusive=tax.inclusive
                )
                tax.tax_id = new_tax.id
                tax.save()
    
    def get(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = Order.objects.get(id=order_id)

        coupons_id_list = [coupon.id for coupon in stripe.Coupon.list()]
        promo_codes = [{promo.code: promo.id} for promo in stripe.PromotionCode.list()]

        for discount in Discount.objects.all():
            if str(discount.id) not in coupons_id_list:
                stripe.Coupon.create(
                    id=str(discount.id),
                    percent_off=discount.percent_off,
                    duration=discount.duration,
                    duration_in_months=discount.duration_in_months
                )
                order.discount.add(discount)
        
        for promo in PromoCode.objects.all():
            check_list = list(filter(lambda x: True if promo.code in x else False, promo_codes))
            if not check_list:
                stripe.PromotionCode.create(
                    coupon=str(promo.coupon.id),
                    code=promo.code
                )
            else:
                stripe.PromotionCode.modify(check_list[0].get(promo.code), metadata={"coupon": promo.coupon.id})

        if request.user.is_authenticated:
            # Tax и настройку скидки делает админ
            tax_order = Tax.objects.filter(jurisdiction=order.jurisdiction).first()
            order.tax = tax_order
            checkout_session = stripe.checkout.Session.create(
            customer_email = order.user.email,
            payment_method_types=['card'],
            allow_promotion_codes=True,
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
                    'tax_rates': [order.tax.tax_id]
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/cancel/',
            )
            order.status = 'STATUS_PAID'
            order.save()
            return JsonResponse({
                'id': checkout_session.id
            })
        else:
            return redirect('home')

