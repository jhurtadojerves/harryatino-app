from django.urls import path

from superadmin.views import (
    ListView,
    CreateView,
    UpdateView,
    MassUpdateView,
    DetailView,
    DeleteView,
    MassDeleteView,
    DuplicateView
)

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
