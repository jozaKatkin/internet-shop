from django.contrib import messages

from core.models import *
from django.shortcuts import get_object_or_404, redirect


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item_in_order = ItemInOrder.objects.create(product=product)
    order_qs = Order.objects.filter(is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product=product):
            pass
        else:
            order.items.add(item_in_order)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
