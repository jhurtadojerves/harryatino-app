"""Sim templatetags"""

# Django
from django import template
from django.db.models import Sum

register = template.Library()


@register.simple_tag
def check_permission(user, permission):
    if user.is_superuser:
        return True
    return user.has_perm(permission)


@register.simple_tag
def concat_all(*args):
    """concatenate all args"""
    return "".join(map(str, args))


@register.simple_tag
def sum_sales_products_queryset(queryset):
    aggregation = queryset.aggregate(Sum("product__points"))
    return aggregation.get("product__points__sum") or 0
