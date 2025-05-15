from django.urls import path

from .views import (
    CountMonthlyPostsForm,
    UpdatePostForm,
    UpdateProfileForm,
    UpdateTopicsForm,
)

urlpatterns = [
    path(
        route="dynamicforms/data/<int:pk>/",
        view=UpdateProfileForm.as_view(),
        name="update_profile",
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
]
