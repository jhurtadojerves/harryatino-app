"""Forms to announcements"""

# Django
from django import forms

# Third party integration
from ckeditor.widgets import CKEditorWidget

# Models
from apps.announcements.models import Announcement


class AnnouncementForm(forms.ModelForm):
    """Forms to create and update announcement"""

    class Meta:
        model = Announcement
        fields = ("name", "content")
        widgets = {"content": CKEditorWidget()}
