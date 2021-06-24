"""Sim templatetags"""
# Django
from django import template
from django.shortcuts import reverse
from django.urls import NoReverseMatch

# Third party integration
from superadmin import site
from superadmin.shortcuts import get_slug_or_pk
from superadmin.templatetags.superadmin_utils import site_url

register = template.Library()


@register.simple_tag()
def insoles_detail(instance):
    model_site = site.get_modelsite(instance.__class__)
    app_name = instance.__class__._meta.app_label
    model_name = instance._meta.model.__name__
    raw_slug_or_pk = get_slug_or_pk(instance, slug_field=model_site.slug_field)
    slug_or_pk = ""
    slug = ""
    for key, value in raw_slug_or_pk.items():
        slug = value
        slug_or_pk = key
    return reverse("insoles_detail", args=(app_name, model_name, slug, slug_or_pk))


@register.simple_tag()
def has_detail_url(instance):
    try:
        site_url(instance, "detail")
        return True
    except Exception as e:
        return False
