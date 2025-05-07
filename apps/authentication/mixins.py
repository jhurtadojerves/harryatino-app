import operator
from functools import reduce

from django.db.models import Q
from django.shortcuts import redirect
from superadmin.templatetags.superadmin_utils import site_url

from apps.authentication.services import AccessTokenService
from apps.utils.services import UserAPIService


class UserListMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(pk=self.request.user.pk)
        return queryset


class UserProfileMixin:
    def get_object(self, queryset=None):
        return self.request.user


class AccessTokenCreateMixin:
    def form_valid(self, form):
        profile = form.cleaned_data.get("wizard")
        self.object = form.save(commit=False)
        profile = UserAPIService.download_user_data_and_update(profile)
        user = AccessTokenService.prepare_profile(profile, str(self.object.token))
        self.object.user = user
        self.object.save()
        self.object.send_message()

        return redirect(site_url(self.object, "detail"))


class AccessTokenListMixin:
    def get_queryset(self):
        search_params_config = (
            "user__profile__nick__unaccent__icontains",
            "user__profile__forum_user_id__icontains",
        )
        queryset = super().get_queryset()
        search_params = self.request.GET

        if search_params:
            params = search_params.dict()
            search = params.pop("search", None)
            params.pop("page", None)
            params.pop("paginate_by", None)
            search = (
                (search.replace("+", ",").replace(";", ",")).split(",")
                if search
                else None
            )

            if search:
                for search_value in search:
                    filters = {
                        key: search_value.strip() for key in search_params_config
                    }
                    params.update(**filters)
                    args = [Q(**{key: value}) for key, value in filters.items()]
                    queryset = queryset.filter(reduce(operator.__or__, args))

        return queryset
