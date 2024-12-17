from django import template

register = template.Library()


@register.filter
def boolean_to_human(value):
    if isinstance(value, bool):
        return "✅" if value else "❌"

    return value
