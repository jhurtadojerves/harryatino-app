"""View to show update profile"""

from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import DetailView
from superadmin.views import DetailView as DetailViewSA

from .models import AccessToken, User
from .sites import UserProfileSite


class UserProfile(DetailViewSA):
    site = UserProfileSite(User)


class LoginWithToken(DetailView):

    model = AccessToken
    slug_field = "token"
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        """Validate user and login"""
        self.object = self.get_object()
        login(request, self.object.user)
        messages.success(request, "Te autenticaste correctamente")
        return redirect("/")
