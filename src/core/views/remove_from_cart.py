from django.contrib import messages
from core.models import *
from django.shortcuts import get_object_or_404, redirect


def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        is_ordered=False,
        user=request.user
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product=product).exists():
            item_in_order = ItemInOrder.objects.filter(
                product=product,
                is_ordered=False,
                user=request.user
            )[0]
            order.items.remove(item_in_order)
            item_in_order.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order_summary_url")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product_detail_url", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product_detail_url", pk=pk)
