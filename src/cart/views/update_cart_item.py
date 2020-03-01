from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from cart.forms import AddToCartForm
from cart.models import CartItem
from cart.utils import get_cart


class UpdateCartItemView(FormView):
    http_method_names = ['post']
    success_url = reverse_lazy('order_summary_url')
    form_class = AddToCartForm
    template_name = 'order_summary.html'
    context_object_name = 'cart'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        cart = get_cart(request)
        cart_item = CartItem.objects.get(cart=cart, pk=self.kwargs['pk'])
        cart_item.quantity = request.POST['cart_item_quantity']
        cart_item.save()
        return self.form_valid(form)

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, "Product quantity has been updated.")
        return super(UpdateCartItemView, self).form_valid(form)

