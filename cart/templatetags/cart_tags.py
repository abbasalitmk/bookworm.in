from django import template
from cart.models import CartItem

register = template.Library()


@register.simple_tag(takes_context=True)
def show_cart_items(context):
    cart_items = CartItem.objects.filter(
        cart=context.request.session.get('cart_id'))
    return {'cart_items': cart_items}
