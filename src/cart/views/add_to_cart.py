from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from cart.forms import AddToCartForm
from cart.models import CartItem
from core.models import *
from django.shortcuts import get_object_or_404, redirect
from cart.utils import get_cart


class AddToCartView(FormView):
    template_name = 'product_detail.html'
    success_url = reverse_lazy('order_summary_url')
    http_method_names = ['post']
    form_class = AddToCartForm

    def form_valid(self, form, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        quantity = form.cleaned_data['quantity']
        cart = get_cart(self.request, create=True)
        cart_item, cart_item_created = CartItem.objects.update_or_create(cart=cart, product=product)
        if cart_item_created is False:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        messages.success(self.request, 'This item was added to your cart.')
        return super(AddToCartView, self).form_valid(form)
