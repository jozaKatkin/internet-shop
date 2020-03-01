from django.views.generic import DetailView

from cart.forms import AddToCartForm
from core.models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = AddToCartForm
        return context


