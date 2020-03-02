from cart.utils import get_cart
from django import template

register = template.Library()


@register.inclusion_tag('cart_item_count.html', takes_context=True)
def cart_item_count(context):
    request = context.get('request')
    cart = get_cart(request)
    quantity = None
    if cart:
        quantity = cart.get_total_quantity_of_items()

    return {
        'cart_item_count': quantity or 0
    }
