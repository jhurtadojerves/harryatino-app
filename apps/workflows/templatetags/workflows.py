from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def transition_perm(user, permission):
    """Check permission workflow"""
    return user.has_perm(f"{permission}")


@register.simple_tag(takes_context=True)
def context_transition_perm(context, list_perm):
    state = False
    if isinstance(list_perm, list):
        state_list = [context.get(perm, False) for perm in list(list_perm)]
        if True in state_list:
            state = True
    if isinstance(list_perm, bool):
        state = list_perm
    return state


@register.simple_tag
def workflow_change_state(instance):
    app_name = instance.__class__._meta.app_label
    model_name = instance._meta.model.__name__
    return reverse("workflow_change_state", args=(app_name, model_name, instance.pk))


@register.simple_tag
def workflow_visible_states(state):
    return state - 1, state, state + 1
