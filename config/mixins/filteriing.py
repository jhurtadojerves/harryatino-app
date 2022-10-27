"""Simple filtering"""

# third party integration
from django.utils.text import slugify
from superadmin import site


class GenericFiltering:
    def get_queryset(self):
        queryset = super().get_queryset()
        search_params = self.request.GET
        if search_params:
            params = search_params.dict()
            search = params.pop("search", None)
            params.pop("page", None)
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


class FilterByChoice:
    CHOICES = []

    def get_search_choices(self, selected_choice=None):
        choices = []
        for choice in self.CHOICES:
            choice_id = choice[0]
            choice_display = choice[1]
            slug = slugify(choice_display.replace("/", " "))
            if selected_choice and selected_choice == slug:
                return choice_id
            choices.append({"id": choice_id, "display": choice_display, "slug": slug})
        return choices

    def get_search_selected_choice(self, selected_choice):
        return self.get_search_choices(selected_choice)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        choice_param = self.request.GET.get("choice_param", None)
        random_labels = ["info", "warning"]
        context.update(
            {
                "search_choices": self.get_search_choices(),
                "choice_param": choice_param,
                "random_labels": random_labels,
            }
        )

        return context
