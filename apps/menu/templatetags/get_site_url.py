"""Sim templatetags"""
# Django
from django import template
from django.urls import NoReverseMatch

# Third party integration
from superadmin import site
from superadmin.shortcuts import get_urls_of_site

# Local
from ..utils import get_site_url as get_url

register = template.Library()


@register.simple_tag()
def get_site_url(instance, action):
    return get_url(instance, action)
