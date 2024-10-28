"""Sites from authentication"""

# Base
from superadmin.decorators import register

from config.base import BaseSite

# Forms
from .forms import AccessTokenForm, UserForm

# Local
from .mixins import (
    AccessTokenCreateMixin,
    AccessTokenListMixin,
    UserListMixin,
    UserProfileMixin,
)


@register("authentication.User")
class UserSite(BaseSite):
    """Site from profiles"""

    form_class = UserForm
    # form_mixins = (UserFormMixin,)
    list_mixins = (UserListMixin,)
    detail_fields = (
        (
            "username",
            "get_full_name:nombre completo",
        ),
        ("email", "old_number"),
    )
    list_fields = ("username:usuario", "email")
    allow_views = ("update", "list", "detail")
    form_template_name = None


class UserProfileSite(UserSite):
    detail_mixins = (UserProfileMixin,)


@register("authentication.AccessToken")
class AccessTokenSite(BaseSite):
    form_class = AccessTokenForm
    form_mixins = (AccessTokenCreateMixin,)
    list_mixins = (AccessTokenListMixin,)
    detail_fields = ("user:Usuario",)
    allow_views = ("create", "list", "detail", "delete")
