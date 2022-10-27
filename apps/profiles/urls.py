# Django
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

# Views
from apps.profiles.views import (
    ProfileCreate,
    ProfileDetail,
    ProfileList,
    ProfileUpdate,
    SocialRankCreate,
    SocialRankDetail,
    SocialRankList,
    SocialRankUpdate,
)
from apps.utils.generate_url import pattern

app_name = "profile"

urlpatterns = [
    path(route="login", view=LoginView.as_view(template_name="auth/login.html")),
    path(route="logout", view=LogoutView.as_view()),
]

urlpatterns += pattern(
    prefix="profile",
    url="mago",
    create_view=ProfileCreate,
    detail_view=ProfileDetail,
    list_view=ProfileList,
    update_view=ProfileUpdate,
)

urlpatterns += pattern(
    prefix="rank",
    url="rango-social",
    create_view=SocialRankCreate,
    detail_view=SocialRankDetail,
    list_view=SocialRankList,
    update_view=SocialRankUpdate,
)
