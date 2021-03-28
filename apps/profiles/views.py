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

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data()
        page = self.request.GET.get("page", 1)
        category = self.request.GET.get("category", False)
        section = self.request.GET.get("section", False)
        sales = self.object.sales.all()
        search_name = False
        search_value = False
        search_url = ""

        if category and Category.objects.filter(name=category.upper()).exists():
            search_url = f"&category={category}"
            search_name = "category"
            search_value = category
            potions = False
            if category in ("P", "PP", "PPP", "PPPP", "PPPPP"):
                category = category.replace("P", "A")
                potions = True
            category = Category.objects.get(name=category.upper())
            sales = self.object.sales.filter(product__category=category,)
            if potions:
                sales = sales.exclude(~Q(product__reference__icontains="P"))
            else:
                sales = sales.exclude(product__reference__icontains="P")

        if section and Section.objects.filter(slug=slugify(section)).exists():
            search_url = f"&section={section}"
            search_name = "section"
            search_value = section
            potions = False
            if section == "Pociones":
                section = "Objetos"
                potions = True
            section = Section.objects.get(slug=slugify(section))
            sales = self.object.sales.filter(product__category__section=section,)
            if potions:
                sales = sales.exclude(~Q(product__reference__icontains="P"))
            else:
                sales = sales.exclude(product__reference__icontains="P")
        pages_url = ""
        paginator = Paginator(sales, per_page=8)
        if int(page) > paginator.num_pages:
            page = paginator.num_pages
        selected_page = paginator.page(page)
        context.update(
            {
                "search_url": f"{pages_url}{search_url}",
                "all_pages": paginator,
                "page_form": page,
                "current_page": selected_page,
                "sections": Section.objects.all(),
                "search_name": search_name,
                "search_value": search_value,
            }
        )
        return context


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
