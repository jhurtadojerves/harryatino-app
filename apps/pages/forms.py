"""Products form"""

# Third party integration
from superadmin.forms import ModelForm

# Local
from apps.pages.models import Page


class PageForm(ModelForm):
    class Meta:
        model = Page
        fieldsets = (
            "name",
            "show_in_home_page",
            "content",
        )
