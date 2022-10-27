# Base
from functools import reduce

from django.contrib.admin.utils import flatten
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured

# Django
from django.urls import path
from django.utils.html import format_html
from superadmin.services import FieldService as BaseFieldService
from superadmin.services import settings

# Third party integration
from superadmin.views import (
    CreateView,
    DeleteView,
    DetailView,
    DuplicateView,
    ListView,
    MassDeleteView,
    MassUpdateView,
    UpdateView,
)

# Local
from config.base import BaseSite


class DefaultSite(BaseSite):
    def get_urls(self):
        urlpatterns = []

        has_slug = hasattr(self.model, self.slug_field)
        route_param = "<slug:slug>" if has_slug else "<int:pk>"

        if "list" in self.allow_views:
            # url_name = "%s_%s_%s" % (*info, self.url_list_suffix)
            url_name = self.get_base_url_name("list")
            urlpatterns += [
                path(route="", view=ListView.as_view(site=self), name=url_name)
            ]

        if "create" in self.allow_views:
            url_create_name = self.get_base_url_name("create")

            urlpatterns += [
                path(
                    route=f"{self.url_create_suffix}/",
                    view=CreateView.as_view(site=self),
                    name=url_create_name,
                ),
            ]

        if "update" in self.allow_views:
            url_update_name = self.get_base_url_name("update")

            urlpatterns += [
                path(
                    route=f"{route_param}/{self.url_update_suffix}/",
                    view=UpdateView.as_view(site=self),
                    name=url_update_name,
                ),
                path(
                    route=f"{self.url_update_suffix}/",
                    view=MassUpdateView.as_view(site=self),
                    name=self.get_base_url_name("mass_update"),
                ),
            ]

        if "detail" in self.allow_views:
            url_detail_name = self.get_base_url_name("detail")
            suffix = self.url_detail_suffix
            detail_route = f"{route_param}/"
            if suffix and suffix != "":
                detail_route += f"{self.url_detail_suffix}/"

            urlpatterns += [
                path(
                    route=detail_route,
                    view=DetailView.as_view(site=self),
                    name=url_detail_name,
                ),
            ]

        if "delete" in self.allow_views:
            url_delete_name = self.get_base_url_name("delete")

            urlpatterns += [
                path(
                    route=f"{route_param}/{self.url_delete_suffix}/",
                    view=DeleteView.as_view(site=self),
                    name=url_delete_name,
                ),
                path(
                    route=f"{self.url_delete_suffix}/",
                    view=MassDeleteView.as_view(site=self),
                    name=self.get_base_url_name("mass_delete"),
                ),
            ]

        urlpatterns += [
            path(
                route=f"{route_param}/{self.url_duplicate_suffix}/",
                view=DuplicateView.as_view(site=self),
                name=self.get_base_url_name("duplicate"),
            ),
        ]
        return urlpatterns


class CustomFieldServiceMixin:
    def get_results(self):
        if isinstance(self.site.detail_fields, (list, tuple)):
            fields = flatten(self.site.detail_fields)
        elif isinstance(self.site.detail_fields, dict):
            fields = reduce(
                lambda acc, fieldset: acc + flatten(fieldset),
                self.site.detail_fields.values(),
                [],
            )
        else:
            raise ImproperlyConfigured(
                "The fieldsets must be an instance of list, tuple or dict"
            )
        fields = fields if fields else (field.name for field in self.model._meta.fields)
        results = {
            field: (
                FieldService.get_field_label(self.object, field),
                FieldService.get_field_value(self.object, field),
                FieldService.get_field_type(self.object, field),
            )
            for field in fields
        }

        flatten_results = results.values()

        def parse(fieldset):
            def wrap(fields):
                fields = fields if isinstance(fields, (list, tuple)) else [fields]
                return {
                    "bs_cols": int(12 / len(fields)),
                    "fields": [results.get(field, ("", "", "")) for field in fields],
                }

            fieldset_list = list(map(wrap, fieldset))
            return fieldset_list

        fieldsets_list = self.site.detail_fields
        fieldsets = (
            [(None, fieldsets_list)]
            if isinstance(fieldsets_list, (list, tuple))
            else fieldsets_list.items()
        )
        fieldsets_results = [
            {"title": title or "", "fieldset": parse(fieldset)}
            for title, fieldset in fieldsets
        ]

        return flatten_results, fieldsets_results


class FieldService(BaseFieldService):
    @classmethod
    def get_field_value(cls, object, field):
        if "__str__" in field:
            return object
        if object is None:
            return object
        field = field.split(cls.LABEL_SEPARATOR)[0]
        names = field.split(cls.FIELD_SEPARATOR)
        name = names.pop(0)
        if not hasattr(object, name):
            raise AttributeError(
                f"Does not exist attribute <{name}> for {str(object)}."
            )
        if len(names):
            attr = getattr(object, name)
            return cls.get_field_value(
                attr() if callable(attr) else attr, cls.FIELD_SEPARATOR.join(names)
            )
        try:
            field = object._meta.get_field(name)
            if hasattr(field, "choices") and field.choices:
                return dict(field.choices).get(field.value_from_object(object))
            elif field.related_model:
                if field.one_to_many or field.many_to_many:
                    raise ImproperlyConfigured(
                        "OneToMany or ManyToMany is not supported: '%s' " % field.name
                    )
                try:
                    return field.related_model.objects.get(
                        pk=field.value_from_object(object)
                    )
                except AttributeError:
                    if field.one_to_one:
                        return getattr(object, field.related_name)
                except field.related_model.DoesNotExist:
                    return None
            else:
                return field.value_from_object(object)
        except FieldDoesNotExist:
            attr = getattr(object, name)
            attr = attr() if callable(attr) else attr
            if isinstance(attr, bool):
                attr = settings.BOOLEAN_YES if attr else settings.BOOLEAN_NO
            return format_html(str(attr))
