from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.views.generic import DetailView
from newrelic import agent

from apps.dynamicforms.models import Form
from apps.dynamicforms.services import FormService
from apps.management.services import ProfileHistoryService
from apps.menu.utils import get_site_url
from apps.utils.services import UserAPIService


class UpdateProfileView(PermissionRequiredMixin, DetailView):
    model = Form
    form_id = 1
    template_name = "insoles/form.html"
    permission_required = "management.can_update_profiles"

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            form_service = FormService(request, self.object)
            forum_user_id = request.GET.get("forum_user_id")
            data = self.get_data(forum_user_id)
            template = form_service.get_form(data=data)
            history = ProfileHistoryService.create(
                forum_user_id=forum_user_id,
                data=data.get("custom_fields"),
            )

            return JsonResponse(
                {
                    "template": template,
                    "history": history.id,
                    "username": data.get("nick"),
                },
                status=200,
            )
        except Exception as e:
            return JsonResponse(
                {
                    "error": str(e),
                },
                status=400,
            )

    def get_object(self):
        queryset = self.get_queryset()
        form_id = self.form_id
        queryset = queryset.filter(id=form_id)

        return queryset.first()

    def get_data(self, forum_user_id):
        return UserAPIService.get_forum_user_data_v2(forum_user_id)

    @staticmethod
    def get_payload(data):
        payload = ""

        for key, value in data.items():
            payload += f"{key}={value}&"
        payload = payload.encode("utf-8")

        return payload

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST.dict()
            history = request.GET.get("history")
            forum_user_id = request.GET.get("forum_user_id")
            data.pop("csrfmiddlewaretoken", None)
            UserAPIService.update_user_profile(
                user_id=forum_user_id,
                raw_data=data,
            )
            history_object = ProfileHistoryService.update(
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
