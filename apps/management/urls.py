from django.urls import path

from apps.management.views import UpdateEntryView, UpdateProfileView

app_name = "management"

urlpatterns = [
    path(
        route="administracion/actualizar-perfil/form/<int:pk>/",
        view=UpdateProfileView.as_view(),
        name="update_profile",
    ),
    path(
        route="administracion/actualizar-topic-y-post/form/<int:pk>/",
        view=UpdateEntryView.as_view(),
        name="update_profile",
    ),
]
