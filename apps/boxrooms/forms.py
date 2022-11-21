"""Products form"""

# Third party integration
from django_select2.forms import ModelSelect2Widget
from superadmin.forms import ModelForm

# Local
from apps.boxrooms.models import Boxroom


class BoxroomForm(ModelForm):
    class Meta:
        model = Boxroom
        fieldsets = (
            "profile",
            "content",
        )
        widgets = {
            "profile": ModelSelect2Widget(
                model="profiles.Profile",
                search_fields=[
                    "nick__unaccent__icontains",
                    "forum_user_id__contains",
                ],
                max_results=20,
                attrs={
                    "data-minimum-input-length": 0,
                },
            ),
        }
