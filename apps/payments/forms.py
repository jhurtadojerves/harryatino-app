# Django
from django import forms

# Third party integration
from django_select2.forms import (
    ModelSelect2Widget,
    ModelSelect2MultipleWidget,
)
from superadmin.forms import ModelForm

# Local
from apps.payments.models import Work


class WorkMonthForm(ModelForm):
    class Meta:
        model = Work
        fieldsets = ("is_active", "wizard", "work", "work_description")
        widgets = {
            "wizard": ModelSelect2Widget(
                model="profiles.Profile",
                search_fields=["nick__icontains", "forum_user_id__icontains"],
                attrs={
                    "data-minimum-input-length": 0,
                },
            ),
        }
