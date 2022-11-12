from superadmin.forms import ModelForm

from .models import Profile


class WizardForm(ModelForm):
    class Meta:
        model = Profile
        fieldsets = ("forum_user_id",)
