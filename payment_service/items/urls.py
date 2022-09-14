from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    Create_Checkout_Session_Item_View,
    Item_Page_View,
    Success_View,
    Cancel_View,
)


urlpatterns = [
    path('buy/<pk>/', Item_Page_View.as_view(), name='main_item_page'),
    path('item/<pk>/',
         Create_Checkout_Session_Item_View.as_view(),
         name='create_session_page'
        ),
    path('cancel/', Cancel_View.as_view(), name='cancel'),
    path('success/', Success_View.as_view(), name='success'),
]