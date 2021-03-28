# Models
from apps.authentication.models import User

# Hydra
from superadmin.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = User
        fieldsets = (("first_name", "last_name"),)


"""
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fieldsets = (("phone_number", "avatar"),)
"""
