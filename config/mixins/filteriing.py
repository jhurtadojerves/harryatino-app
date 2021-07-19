"""Simple filtering"""
# Django
from django.db.models import Q

# third party integration
from superadmin import site


class GenericFiltering:
    def get_queryset(self):
        queryset = super().get_queryset()
        search_params = self.request.GET
        if search_params:
            params = search_params.dict()
            search = params.pop("search", None)
            model_site = site.get_modelsite(self.model)
            if (
                search
                and hasattr(model_site, "search_param")
                and isinstance(model_site.search_param, str)
            ):
                params.update({f"{model_site.search_param}__icontains": search})
            queryset = queryset.filter(**params)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_params = self.request.GET
        if search_params:
            params = search_params.dict()
            search = params.pop("search", None)
            context.update({"params": params})
            if search:
                context.update({"search": search})
        return context
