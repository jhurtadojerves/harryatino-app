from datetime import datetime

from django import template

register = template.Library()


@register.filter
def format_if_date(value, fmt="%d/%m/%Y %H:%M"):
    try:
        value_str = str(value).split("+")[0].split(".")[0]
        parsed = datetime.strptime(value_str, "%Y-%m-%d %H:%M:%S")
        return parsed.strftime(fmt)
    except (ValueError, TypeError):
        return value
