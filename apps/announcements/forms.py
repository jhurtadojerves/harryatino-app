"""Forms to announcements"""

# Django
# Third party integration
from ckeditor.widgets import CKEditorWidget
from django import forms

# Models
from apps.announcements.models import Announcement


class AnnouncementForm(forms.ModelForm):
    """Forms to create and update announcement"""

    class Meta:
        model = Announcement
        fields = ("name", "content")
        widgets = {"content": CKEditorWidget()}
