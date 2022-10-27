"""Views for boxrooms"""

# Base Views
# Models
from apps.boxrooms.models import Boxroom
from apps.utils.views import (
    GenericCreateView,
    GenericDetailView,
    GenericListView,
    GenericUpdateView,
)


class BoxroomCreate(GenericCreateView):
    """Boxroom Create View"""

    model = Boxroom
    fields = "__all__"
    prefix = "boxroom"
    app_name = "boxroom"

    def get_success_url(self):
        return self.object.get_absolute_url()


class BoxroomUpdate(GenericUpdateView):
    """Boxroom Create View"""

    model = Boxroom
    fields = "__all__"
    prefix = "boxroom"
    app_name = "boxroom"

    def get_success_url(self):
        return self.object.get_absolute_url()


class BoxroomDetail(GenericDetailView):
    """Boxroom Create View"""

    model = Boxroom
    fields = "__all__"
    context_object_name = "boxroom"
    template_name = "boxrooms/boxroom_detail.html"


class BoxroomList(GenericListView):
    """Boxroom Create View"""

    model = Boxroom
    context_object_name = "boxrooms"
    list_display = ("profile", "slug")
