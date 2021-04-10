# Django
from django.urls import path

# Views
from apps.announcements.views import (
    AnnouncementCreate,
    AnnouncementDetail,
    AnnouncementList,
    AnnouncementUpdate,
)

from apps.utils.generate_url import pattern

app_name = "announcement"

urlpatterns = [] + pattern(
    prefix="announcement",
    url="anuncio",
    create_view=AnnouncementCreate,
    detail_view=AnnouncementDetail,
    list_view=AnnouncementList,
    update_view=AnnouncementUpdate,
)
