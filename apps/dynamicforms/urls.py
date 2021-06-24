# Django
from django.urls import path

# Views
from .views import (
    UpdateProfileForm,
    UpdateLevelsForm,
    UpdateTopicsForm,
    CountMonthlyPostsForm,
)

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
    path(
        route="dynamicforms/posts/<int:pk>/",
        view=CountMonthlyPostsForm.as_view(),
        name="count_posts",
    ),
]
