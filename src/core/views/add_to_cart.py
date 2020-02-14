from django.contrib import messages

from core.models import *
from django.shortcuts import get_object_or_404, redirect


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    item_in_order, created = ItemInOrder.objects.get_or_create(
        is_ordered=False,
        product=product,

    )
    order_qs = Order.objects.filter(is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product=product.pk).exists():
            item_in_order.quantity += 1
            item_in_order.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("product_detail_url", pk=product_id)
        else:
            order.items.add(item_in_order)
            messages.info(request, "This item was added to your cart.")
            return redirect("product_detail_url", pk=product_id)
