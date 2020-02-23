from core.models import Order
from django import template

register = template.Library()


@register.filter(name='cart_item_count')
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, is_ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

