from django.urls import path

from .views import OrderHistoryListView, add_item_to_cart, Order_Page_View, Create_Checkout_Session_Order_View, cart_view, CartDeleteItem


urlpatterns = [
    path('history/', OrderHistoryListView.as_view(), name ='history'),
    path('add-item-to-cart/<int:pk>/', add_item_to_cart, name='add_item_to_cart'),
    path('cart_view/',
         cart_view, name='cart_view'),
    path('delete_item/<int:pk>', CartDeleteItem.as_view(), name='cart_delete_item'),
    path('cart/<int:pk>/', Order_Page_View.as_view(), name='order_detail'),
    path('order/<int:pk>',
         Create_Checkout_Session_Order_View.as_view(),
         name='create_session_order_page'
        ),
]