from django.contrib import messages

from core.models import *
from django.shortcuts import get_object_or_404, redirect


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item_in_order, created = ItemInOrder.objects.get_or_create(
        is_ordered=False,
        product=product,
        user=request.user
    )
    order_qs = Order.objects.filter(is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product=product).exists():
            item_in_order.quantity += 1
            item_in_order.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order_summary_url")
        else:
            order.items.add(item_in_order)
            messages.info(request, "This item was added to your cart.")
            return redirect("order_summary_url")
    else:
        ordered_at = timezone.now()
        order = Order.objects.create(user=request.user, ordered_at=ordered_at)
        order.items.add(item_in_order)
        messages.info(request, "This item was added to your cart.")
        return redirect("order_summary_url")
