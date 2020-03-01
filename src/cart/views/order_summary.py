from django.views.generic import TemplateView
from django.shortcuts import render

from cart.utils import get_cart
from core.models import Order
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


class OrderSummaryView(TemplateView):
    template_name = 'order_summary.html'

    def get_context_data(self, **kwargs):
        context = super(OrderSummaryView, self).get_context_data(**kwargs)
        cart = get_cart(self.request)
        items = []
        if cart:
            items = cart.items.all()
        context.update({
            'cart': cart,
            'cart_items': items
        })
        return context

        # try:
        #     order = Order.objects.get(user=self.request.user, is_ordered=False)
        #     context = {
        #         'order': order
        #     }
        #     return render(self.request, 'order_summary.html', context)
        # except ObjectDoesNotExist:
        #     messages.warning(self.request, "You do not have an active order")
        #     return redirect("/")

