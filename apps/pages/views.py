"""Views for pages"""

# Django views
from django.views.generic import TemplateView

# Views
from apps.utils.views import (
    GenericCreateView,
    GenericDetailView,
    GenericListView,
    GenericUpdateView,
)

from apps.pages.models import Page


class PageCreate(GenericCreateView):
    """Page Create View"""

    model = Page
    fields = "__all__"
    prefix = "page"
    app_name = "page"
    slug = True
    template_name = "pages/pages_form.html"


class PageUpdate(GenericUpdateView):
    """Page Create View"""

    model = Page
    fields = "__all__"
    prefix = "page"
    app_name = "page"
    slug = True
    template_name = "pages/pages_form.html"


class PageDetail(GenericDetailView):
    """Page Create View"""

    model = Page
    fields = "__all__"
    context_object_name = "page"
    template_name = "pages/pages_detail.html"


class PageList(GenericListView):
    """Page Create View"""

    model = Page
    context_object_name = "pages"
    paginate_by = 20
    list_display = ("name", "show_in_home_page")
    template_name = "pages/pages_list.html"


class HomePage(TemplateView):
    """Define Home Page"""

    template_name = "pages/pages_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(
            {
                "page": Page.objects.get(show_in_home_page=True)
                if Page.objects.filter(show_in_home_page=True)
                else False
            }
        )
        return context
