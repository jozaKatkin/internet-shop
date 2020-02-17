from django.views.generic import DetailView
from core.models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'core/product_detail.html'


