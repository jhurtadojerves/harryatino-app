# Django
from django import forms
from django.forms import inlineformset_factory

# Third party integration
from django_select2.forms import (
    ModelSelect2Widget,
    ModelSelect2MultipleWidget,
)
from superadmin.forms import ModelForm

from .models import Profile


class WizardForm(ModelForm):
    class Meta:
        model = Profile
        fieldsets = (
            "forum_user_id",
            "nick",
            "magic_level",
            "range_of_creatures",
            "range_of_objects",
            "vault_number",
            "avatar",
        )
