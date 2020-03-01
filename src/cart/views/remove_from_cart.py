from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from cart.models import CartItem
from cart.utils import get_cart


class RemoveFromCartView(DeleteView):
    model = CartItem
    success_url = reverse_lazy('order_summary_url')
    success_message = "The item has been deleted from your cart."
    http_method_names = ['post']

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(RemoveFromCartView, self).delete(self.request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        cart = get_cart(self.request)
        return CartItem.objects.get(cart=cart, pk=self.kwargs['pk'])

