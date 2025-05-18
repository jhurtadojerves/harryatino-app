from django.urls import path

from apps.management.views import UpdateProfileView

app_name = "management"

urlpatterns = [
    path(
        route="administracion/actualizaciones-de-perfil/form/<str:id>/",
        view=UpdateProfileView.as_view(),
        name="update_profile",
    ),
]
