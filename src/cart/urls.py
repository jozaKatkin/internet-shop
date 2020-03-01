from django.urls import path
from .views import *

urlpatterns = [
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary_url'),
    path('add_to_cart/<int:pk>', AddToCartView.as_view(), name='add_to_cart_url'),
    path('remove_from_cart/<int:pk>', RemoveFromCartView.as_view(), name='remove_url'),
    path('update_cart_item/<int:pk>', UpdateCartItemView.as_view(), name='update_url'),
]
