from django import template

from apps.utils.services import LinkService

register = template.Library()


@register.simple_tag
def get_shortcut_url(link):
    return LinkService.get_resolved_short_url(link)
