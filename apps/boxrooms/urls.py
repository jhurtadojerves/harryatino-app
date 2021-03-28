# Django
from django.urls import path

# Views
from apps.boxrooms.views import (
    BoxroomCreate,
    BoxroomDetail,
    BoxroomList,
    BoxroomUpdate,
)

from apps.utils.generate_url import pattern

app_name = "boxroom"

urlpatterns = [] + pattern(
    prefix="boxroom",
    url="trastero",
    slug=True,
    create_view=BoxroomCreate,
    detail_view=BoxroomDetail,
    list_view=BoxroomList,
    update_view=BoxroomUpdate,
)
