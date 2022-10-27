from django import template

register = template.Library()


@register.simple_tag
def is_in_checkout(user, product):
    """Verify if product is in checkout"""
    purchase = user.purchase()
    line = purchase.lines.filter(product_id=product.id)
    if line.exists():
        return line.first()
    return False
