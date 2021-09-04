# Django
from django.urls import path

# Views
from .views import (
    UpdateProfileForm,
    UpdateLevelsForm,
    UpdateTopicsForm,
    UpdatePostForm,
    CountMonthlyPostsForm,
    GetVault,
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
        route="dynamicforms/posts_update/<int:pk>/",
        view=UpdatePostForm.as_view(),
        name="update_posts",
    ),
    path(
        route="dynamicforms/posts/<int:pk>/",
        view=CountMonthlyPostsForm.as_view(),
        name="count_posts",
    ),
    path(
        route="dynamicforms/vaults/update/",
        view=GetVault.as_view(),
        name="update_vaults",
    ),
]
