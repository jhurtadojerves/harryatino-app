"""View to show update profile"""

from superadmin.views import DetailView
from .sites import UserProfileSite
from .models import User


class UserProfile(DetailView):
    site = UserProfileSite(User)
