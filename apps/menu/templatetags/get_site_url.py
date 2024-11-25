"""Sim templatetags"""

# Django
from django import template

# Local
from ..utils import get_site_url as get_url

register = template.Library()


@register.simple_tag()
def get_site_url(instance, action):
    return get_url(instance, action)
