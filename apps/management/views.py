from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.views.generic import DetailView
from newrelic import agent

from apps.dynamicforms.models import Form
from apps.dynamicforms.services import FormService
from apps.management.services import EntryHistoryService, ProfileHistoryService
from apps.menu.utils import get_site_url
from apps.utils.services import PostAPIService, TopicAPIService, UserAPIService


class BaseView(PermissionRequiredMixin, DetailView):
    model = Form
    form_id = None
    data = {}
    template_name = "insoles/form.html"

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            forum_id = request.GET.get("forum_id")
            data = self.get_data(forum_id, request.GET.dict())
            history_id = 0

            if forum_id:
                history = self.create_history(forum_id=forum_id, data=data)
                history_id = history.id

            data.update({"history_id": history_id})
            template = self.get_form_template(request, data)

            return self.get_response(
                template=template, history_id=history_id, data=data
            )
        except Exception as e:
            return JsonResponse(
                {
                    "error": str(e),
                },
                status=400,
            )

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST.dict()
            history = data.get("history_id")
            forum_id = data.get("forum_id")
            data.pop("csrfmiddlewaretoken", None)
            data.pop("forum_id", None)
            data.pop("history_id", None)
            updated_data = self.update_data(forum_id, data)

            if updated_data:
                data.update(updated_data)

            history_object = self.update_history(
                history_id=history,
                data=data,
            )
            return JsonResponse(
                {
                    "status": 200,
                    "message": "Perfil actualizado",
                    "redirect_url": get_site_url(history_object, "detail"),
                }
            )
        except Exception as e:
            request_id = getattr(request, "request_id", "UNKNOWN")
            agent.add_custom_parameter("request_id", request_id)
            agent.add_custom_parameter("path", request.path)
            agent.add_custom_parameter("method", request.method)
            agent.add_custom_parameter(
                "user_id", getattr(getattr(request, "user", None), "id", None)
            )
            agent.record_exception(exc=e)
            return JsonResponse(
                {
                    "status": 403,
                    "message": f"Hubo un problema al procesar tu solicitud (Código: {request_id})",
                },
                status=400,
            )

    def get_object(self):
        if not self.form_id:
            return super().get_object()

        queryset = self.get_queryset()
        queryset = queryset.filter(id=self.form_id)

        return queryset.first()

    def get_form_template(self, request, form_data: dict) -> str:
        self.object = self.get_object()
        self.form_service = FormService(request, self.object)
        template = self.form_service.get_form(data=form_data)

        return template

    def get_data(self, *args, **kwargs):
        raise NotImplementedError("get_data method must be implemented in subclasses")

    def get_response(self, *args, **kwargs) -> JsonResponse:
        raise NotImplementedError(
            "get_response method must be implemented in subclasses"
        )

    def update_data(self, *args, **kwargs):
        raise NotImplementedError(
            "update_data method must be implemented in subclasses"
        )

    def create_history(self, *args, **kwargs):
        raise NotImplementedError(
            "create_history method must be implemented in subclasses"
        )

    def update_history(self, *args, **kwargs):
        raise NotImplementedError(
            "update_history method must be implemented in subclasses"
        )


class UpdateProfileView(BaseView):
    permission_required = "management.can_update_profiles"

    def get_data(self, forum_user_id, _: dict = {}):
        if forum_user_id:
            data = UserAPIService.get_forum_user_data_v2(forum_user_id)
            data.update(
                {
                    "forum_id": forum_user_id,
                }
            )
            self.data = data

        return self.data

    def get_response(
        self, template: str, history_id: int, data: dict = {}
    ) -> JsonResponse:
        title = self.data.get("nick", "") or ""

        if title:
            title = f"de {title}"

        return JsonResponse(
            {
                "template": template,
                "history": history_id,
                "title": title,
            },
            status=200,
        )

    def create_history(self, forum_id: int, data: dict):
        return ProfileHistoryService.create(
            forum_user_id=forum_id,
            data=data,
        )

    def update_data(self, forum_id: int, data: dict):
        UserAPIService.update_user_profile(
            user_id=forum_id,
            raw_data=data,
        )

    def update_history(self, history_id: int, data: dict):
        return ProfileHistoryService.update(
            history_id=history_id,
            data=data,
        )


class UpdateEntryView(BaseView):
    permission_required = "management.can_update_entries"

    def create_history(self, forum_id: int, data: dict):
        new_data = data.copy()
        type = new_data.pop("type", "topic").lower()

        return EntryHistoryService.create(
            entry_id=forum_id,
            data=new_data,
            type=type,
        )

    def update_history(self, history_id: int, data: dict):
        return EntryHistoryService.update(history_id=history_id, data=data)

    def get_data(self, forum_id: int, request_data: dict = {}):
        data = {}

        if forum_id and request_data:
            type = request_data.get("type", "Topic")

            if type.lower() == "topic":
                data = TopicAPIService.get_topic_data(forum_id)
            else:
                data = PostAPIService.get_data(forum_id)

            data.update(
                {
                    "forum_id": forum_id,
                    "author_id": data.get("author", {}).get("id", ""),
                    "author_name": data.get("author", {}).get("name", ""),
                    "type": type,
                }
            )

        return data

    def update_data(self, forum_id: int, data: dict):
        type = data.pop("type")
        author_id = data.get("author_id", None)
        data.update({"author": author_id})

        if type.lower() == "topic":
            new_data = TopicAPIService.update_topic(forum_id, data)
            first_post = new_data.get("firstPost", {})
            author = first_post.get("author", {})
        else:
            new_data = PostAPIService.update_post(forum_id, data)
            author = new_data.get("author", {})

        return {"author_name": author.get("name", "")}

    def get_response(
        self, template: str, history_id: int, data: dict = {}
    ) -> JsonResponse:
        title = data.get("type", "")

        return JsonResponse(
            {
                "template": template,
                "history": history_id,
                "title": f"del {title}" if title else "",
            },
            status=200,
        )
