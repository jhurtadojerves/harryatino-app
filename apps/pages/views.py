"""Views for pages"""

# Django views
from django.views.generic import TemplateView
from django.contrib import messages

from apps.pages.models import Page


class HomePage(TemplateView):
    """Define Home Page"""

    template_name = "pages/page_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pages = Page.objects.filter(show_in_home_page=True)
        page = pages.first() if pages else False
        context.update(
            {
                "page": page,
                "object": page
            }
        )
        return context
