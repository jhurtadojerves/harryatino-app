import operator
from functools import reduce
from django.db.models import Q


class BoxroomListMixin:
    def get_queryset(self):
        search_params_config = (
            "profile__nick__unaccent__icontains",
            "profile__forum_user_id__icontains",
        )
        queryset = super().get_queryset()
        search_params = self.request.GET
        if search_params:
            params = search_params.dict()
            search = params.pop("search", None)
            params.pop("page", None)
            params.pop("paginate_by", None)
            model_site = self.site
            search = (search.replace("+", ",").replace(";", ",")).split(",") if search else None
            if search:
                for search_value in search:
                    filters = {key: search_value.strip() for key in search_params_config}
                    params.update(**filters)
                    args = [Q(**{key: value}) for key, value in filters.items()]
                    queryset = queryset.filter(reduce(operator.__or__, args))
        return queryset


class BoxroomDetailMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        new_format = "nuevo"
        boxroom_format = self.request.GET.get("format", "nuevo")

        if boxroom_format == new_format:
            boxroom_format = True
        else:
            boxroom_format = False

        context.update({"boxroom_format": boxroom_format})
        return context
