from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page_url'),
    path('pierogi/', PierogiView.as_view(), name='pierogi_url'),
    path('bulki/', BulkiView.as_view(), name='bulki_url'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail_url'),
    path('add_to_cart/<int:pk>', add_to_cart, name='add_to_cart_url'),
    path('remove_from_cart/<int:pk>', remove_from_cart, name='remove_url'),
    path('remove_1_pcs/<int:pk>', remove_1_pcs_from_cart, name='remove_1_pcs_url'),
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary_url'),
    path('checkout/', RegisteredUserCheckoutView.as_view(), name='checkout_url'),
    path('success/', SuccessView.as_view(), name='success_url')
]