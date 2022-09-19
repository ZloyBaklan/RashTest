from django.urls import path

from .views import (
    Item_Page_View,
    Success_View,
    Cancel_View,
    ItemListView,
    ItemCreateView,
    create_checkout_session
)

urlpatterns = [
    path('', ItemListView.as_view(), name='home'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('buy/<pk>/', Item_Page_View.as_view(), name='detail'),
    path('item/<pk>/',
         create_checkout_session,
         name='create_session_page'
        ),
    path('success/', Success_View.as_view(), name='success'),
    path('cancel/', Cancel_View.as_view(), name='cancel'),
]