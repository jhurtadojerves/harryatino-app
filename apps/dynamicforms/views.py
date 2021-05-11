"""Views to custom forms"""

# Django
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView

# Local
from apps.dynamicforms.forms import CreationDynamicForm
from .models import Form, AuditAPI

# Third party integration
import requests
from environs import Env

env = Env()
API_KEY_GET = env("API_KEY_GET")
API_KEY_POST = env("API_KEY_POST")


class MixinDynamicForm:
    """Mixin form create dynamic form"""

    METHOD_ACCEPT = ["POST", "PUT"]

    def _get_form_kwargs(self, attr, data=dict):
        kwargs = {"initial": data}
        if self.request.method in self.METHOD_ACCEPT:
            kwargs.update(
                {"data": self.request.POST, "files": self.request.FILES,}
            )
        if hasattr(self, "object"):
            kwargs.update(**attr)
        return kwargs

    def _get_form(self, form_class, attr, data=dict):
        """Return an instance of the form to be used in this view."""
        return form_class(**self._get_form_kwargs(attr, data))


class ShowForm(MixinDynamicForm, DetailView):
    # permission_required = "procedures.change_assignmentofprocedure"
    http_method_names = ["get", "post"]
    model = Form
    form_class = CreationDynamicForm
    template_name = "insoles/form.html"

    def get_user_data(self, user_id):
        payload = {}
        headers = {}
        url = (
            f"https://www.harrylatino.org/api/core/members/{user_id}?key={API_KEY_GET}"
        )
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        custom_fields = data["customFields"]
        raw_user_data = dict()
        for raw in custom_fields.values():
            raw_user_data.update(raw["fields"])
        username = data["name"]
        user_data = dict()
        for key, value in raw_user_data.items():
            user_data.update({f"customFields[{key}]": value["value"]})
        return user_data, username

    def get_form(self, user_id):
        attr = {"form": self.object}
        data, username = self.get_user_data(user_id)
        form = self._get_form(self.form_class, attr, data)
        return form, username, data

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.GET.get("user_id")
            self.object = self.get_object()
            form, username, data = self.get_form(user_id)
            create_url = reverse_lazy("data_url", args=[self.object.pk])
            template = render_to_string(self.template_name, context={"form": form})
            data = {"data": data, "user_id": user_id}
            AuditAPI.objects.create(username=request.user, data=data, action="obtener")
            return JsonResponse(
                {"create_url": create_url, "template": template, "username": username},
                status=200,
            )
        except ValueError:
            return JsonResponse({}, status=500)

    def perform_post(self):
        self.object = self.get_object()
        form = self.get_form()
        action = False
        if not form.is_valid():
            return JsonResponse({"message": "Formulario invalido"}, status=400)

        if form.is_valid():
            action = "editing"
            self.object.data = form.save()
            if "finish" in self.request.POST:
                action = "finish"
                self.object.status = False
            self.object.save()
        return JsonResponse({"action": action}, status=200)

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        user_id = request.GET.get("user_id")
        payload = ""
        del data["csrfmiddlewaretoken"]
        for key, value in data.items():
            payload += f"{key}={value}&"
        payload = payload.encode("utf-8")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        url = (
            f"https://www.harrylatino.org/api/core/members/{user_id}?key={API_KEY_POST}"
        )
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            data = {"data": data, "user_id": user_id}
            AuditAPI.objects.create(username=request.user, data=data, action="guardar")
            return JsonResponse(
                {"status": 200, "message": "Datos actualizados correctamente"}
            )
        else:
            return JsonResponse({"status": 403, "message": "Sucedió un error"})
