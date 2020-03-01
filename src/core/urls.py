from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page_url'),
    path('pierogi/', PierogiView.as_view(), name='pierogi_url'),
    path('bulki/', BulkiView.as_view(), name='bulki_url'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail_url'),
    path('registered_user_checkout/', login_required(RegisteredCheckoutView.as_view()), name='registered_checkout_url'),
    path('anonymous_user_checkout/', AnonymousCheckoutView.as_view(), name='anonymous_checkout_url'),
    path('success/<int:pk>/', SuccessView.as_view(), name='success_url')
]