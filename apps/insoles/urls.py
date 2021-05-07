# Django
from django.urls import path

# Views
from apps.insoles.views import RenderFormView, RenderFieldView

urlpatterns = [
    path(
        route="insoles/forms/<slug:app>/<slug:model>/",
        view=RenderFormView.as_view(),
        name="insoles_form",
    ),
    path(
        route="insoles/forms/<slug:app>/<slug:model>/<slug:field>/",
        view=RenderFieldView.as_view(),
        name="insoles_field",
    ),
]
