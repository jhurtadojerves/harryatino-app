"""Profile admin."""
from django.contrib import admin

# Models
from apps.profiles.models import Profile, SocialRank

# Third party integration
from import_export.admin import ImportExportModelAdmin


@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    """Profile admin."""

    list_display = (
        "nick",
        "forum_user_id",
        "magic_level",
        "range_of_creatures",
        "range_of_objects",
    )
    search_fields = ("nick", "forum_user_id")


@admin.register(SocialRank)
class SocialRankAdmin(ImportExportModelAdmin):
    """Profile admin."""

    list_display = (
        "name",
        "initial_points",
        "end_points",
    )
