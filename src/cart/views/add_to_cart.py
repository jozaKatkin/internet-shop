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


# def add_to_cart(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     item_in_order, created = ItemInOrder.objects.get_or_create(
#         is_ordered=False,
#         product=product,
#         user=request.user
#     )
#     order_qs = Order.objects.filter(is_ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         if order.items.filter(product__pk=product.pk).exists():
#             item_in_order.quantity += 1
#             item_in_order.save()
#             messages.info(request, "This item quantity was updated.")
#             return redirect("order_summary_url")
#         else:
#             order.items.add(item_in_order)
#             messages.info(request, "This item was added to your cart.")
#             return redirect("order_summary_url")
#     else:
#         ordered_at = timezone.now()
#         order = Order.objects.create(user=request.user, ordered_at=ordered_at)
#         order.items.add(item_in_order)
#         messages.info(request, "This item was added to your cart.")
#         return redirect("order_summary_url")
