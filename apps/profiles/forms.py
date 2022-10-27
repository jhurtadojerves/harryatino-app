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
            "avatar",
            "vault_number",
            "boxroom_number",
            "character_sheet",
        )
