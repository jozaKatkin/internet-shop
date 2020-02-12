from django.urls import path
from core.views.product_detail import ProductDetailView
from core.views.main_page import MainPageView

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page_url'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail_url'),
]