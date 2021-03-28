# Django
from django.urls import path

# Views
from apps.pages.views import (
    PageCreate,
    PageDetail,
    PageList,
    PageUpdate,
)

from apps.utils.generate_url import pattern

app_name = "page"

urlpatterns = [] + pattern(
    prefix="page",
    url="pagina",
    create_view=PageCreate,
    detail_view=PageDetail,
    list_view=PageList,
    update_view=PageUpdate,
    slug=True,
)
