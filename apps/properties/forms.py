"""Products form"""

# Third party integration
from ckeditor.widgets import CKEditorWidget
from django_select2 import forms as s2forms
from superadmin.forms import ModelForm

from apps.profiles.models import Profile

# Local
from apps.properties.models import Property


class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fieldsets = (
            ("name", "owner", "property_type"),
            ("vault", "inscription", "rol"),
            "content",
            "is_active",
        )
        widgets = {
            "content": CKEditorWidget(),
            "owner": s2forms.ModelSelect2MultipleWidget(
                model=Profile,
                search_fields=["forum_user_id__icontains", "nick__icontains"],
            ),
        }
