"""Sites from authentication"""

# Base
from superadmin.decorators import register
from config.base import BaseSite

# Forms
from .forms import UserForm

# Local
from .mixins import UserListMixin, UserProfileMixin


@register("authentication.User")
class UserSite(BaseSite):
    """Site from profiles"""

    form_class = UserForm
    # form_mixins = (UserFormMixin,)
    list_mixins = (UserListMixin,)
    detail_fields = (
        ("username", "get_full_name:nombre completo",),
        ("email", "old_number"),
    )
    list_fields = ("get_full_name:nombre completo", "email")
    allow_views = ("update", "list", "detail")
    form_template_name = None


class UserProfileSite(UserSite):
    detail_mixins = (UserProfileMixin,)
