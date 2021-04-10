"""Views for wizards"""

# Django
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.db.models import Q

# Models
from apps.profiles.models import Profile
from apps.products.models import Category, Section

# Views
from apps.utils.views import (
    GenericCreateView,
    GenericDetailView,
    GenericListView,
    GenericUpdateView,
)

from apps.profiles.models import Profile, SocialRank


class ProfileCreate(GenericCreateView):
    """Profile Create View"""

    model = Profile
    fields = "__all__"
    prefix = "profile"
    app_name = "profile"


class ProfileUpdate(GenericUpdateView):
    """Profile Create View"""

    model = Profile
    fields = "__all__"
    prefix = "profile"
    app_name = "profile"


class ProfileDetail(GenericDetailView):
    """Profile Create View"""

    model = Profile
    fields = "__all__"
    context_object_name = "profile"
    template_name = "profiles/profiles_detail.html"


class ProfileList(GenericListView):
    """Profile Create View"""

    model = Profile
    template_name = "profiles/profiles_list.html"
    context_object_name = "profiles"
    paginate_by = 20
    list_display = (
        "id",
        "forum_user_id",
        "nick",
        "magic_level",
        "range_of_creatures",
        "range_of_objects",
        "vault",
    )


class SocialRankCreate(GenericCreateView):
    """SocialRank Create View"""

    model = SocialRank
    fields = "__all__"
    prefix = "rank"
    app_name = "rank"


class SocialRankUpdate(GenericUpdateView):
    """SocialRank Create View"""

    model = SocialRank
    fields = "__all__"
    prefix = "rank"
    app_name = "rank"


class SocialRankDetail(GenericDetailView):
    """SocialRank Create View"""

    model = SocialRank
    fields = "__all__"
    context_object_name = "rank"


class SocialRankList(GenericListView):
    """SocialRank Create View"""

    model = SocialRank
    template_name = "ranks/ranks_list.html"
    context_object_name = "ranks"
    paginate_by = 20
    list_display = (
        "name",
        "initial_points",
        "end_points",
        "slug",
    )
