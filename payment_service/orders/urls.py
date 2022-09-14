from cgi import test
from django.urls import include, path 

from .views import Order_Page_View, Create_Checkout_Session_Order_View


urlpatterns = [
    path('order_buy/<pk>/', Order_Page_View.as_view(), name='main_order_page'),
    path('order/<pk>/',
         Create_Checkout_Session_Order_View.as_view(),
         name='create_session_order_page'
        ),
    ]