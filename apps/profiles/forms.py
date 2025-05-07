from django import forms
from superadmin.forms import ModelForm

from .models import Profile


class WizardForm(ModelForm):
    forum_user_id = forms.CharField()

    class Meta:
        model = Profile
        fieldsets = ("forum_user_id",)

    def clean_forum_user_id(self):
        data = self.cleaned_data["forum_user_id"].strip()  # elimina espacios
        if not data.isdigit():
            raise forms.ValidationError("Solo se permiten números.")
        return int(data)
