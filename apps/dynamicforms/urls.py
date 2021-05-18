# Django
from django.urls import path

# Views
from .views import UpdateProfileForm, UpdateLevelsForm, UpdateTopicsForm

urlpatterns = [
    path(
        route="dynamicforms/data/<int:pk>/",
        view=UpdateProfileForm.as_view(),
        name="update_profile",
    ),
    path(
        route="dynamicforms/levels/<int:pk>/",
        view=UpdateLevelsForm.as_view(),
        name="update_levels",
    ),
    path(
        route="dynamicforms/topics/<int:pk>/",
        view=UpdateTopicsForm.as_view(),
        name="update_topics",
    ),
]
