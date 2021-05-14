"""Views to custom forms"""
# Python
from datetime import datetime

# Django
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView

# Local
from apps.dynamicforms.forms import CreationDynamicForm
from .models import Form, AuditAPI, Action

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

    def _get_form(self, form_class, attr, data):
        """Return an instance of the form to be used in this view."""
        return form_class(**self._get_form_kwargs(attr, data))


class BaseForm(MixinDynamicForm, DetailView):
    http_method_names = ["get", "post"]
    model = Action
    form_class = CreationDynamicForm
    template_name = "insoles/form.html"
    BASE_API_URL = "https://www.harrylatino.org/api/core/members/"


class UpdateProfileForm(BaseForm):
    def get_form(self, user_id):
        attr = {"form": self.object.form}
        data, username = get_user_data(self.BASE_API_URL, user_id)
        form = self._get_form(self.form_class, attr, data)
        return form, username, data

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.GET.get("user_id")
            self.object = self.get_object()
            form, username, data = self.get_form(user_id)
            create_url = reverse_lazy(self.object.path, args=[self.object.pk])
            template = render_to_string(self.template_name, context={"form": form})
            data = {"data": data, "user_id": user_id}
            AuditAPI.objects.create(username=request.user, data=data, action="obtener")
            return JsonResponse(
                {"create_url": create_url, "template": template, "username": username},
                status=200,
            )
        except ValueError:
            return JsonResponse({}, status=500)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = request.POST.dict()
        user_id = request.GET.get("user_id", False)
        del data["csrfmiddlewaretoken"]

        url = (
            f"https://www.harrylatino.org/api/core/members/{user_id}?key={API_KEY_POST}"
        )
        response = post_request(url, get_payload(data))
        return get_response(
            request.user, response, data, user_id, "guardar", "Información actualizada"
        )


class UpdateLevelsForm(BaseForm):
    """Get data for update levels"""

    API_KEY = "a558a350a81d71e06a6d0ae449d9d773"
    # activity_after

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.GET.get("user_id")
            self.object = self.get_object()
            now = datetime.now()
            previous_date = now.replace(day=1, month=now.month - 3)
            previous_date = now.replace(day=now.day - 5)
            timestamp = datetime.timestamp(previous_date)
            members = get_full_user_data(self.BASE_API_URL, timestamp)
            for member in members:
                payload = calculate_level(self.BASE_API_URL, member)

            AuditAPI.objects.create(
                username=request.user, data={members}, action="Niveles actualizados"
            )
            return JsonResponse({"status": 200, "message": "Niveles actualizados"})
        except ValueError:
            return JsonResponse({}, status=500)


def post_request(url, data):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.request("POST", url, headers=headers, data=data)
    return response


def get_response(user, response, data, user_id, action, message):
    if response.status_code == 200:
        data = {"data": data, "user_id": user_id}
        AuditAPI.objects.create(username=user, data=data, action=action)
        return JsonResponse({"status": 200, "message": message})
    else:
        return JsonResponse({"status": 403, "message": "Sucedió un error"})


def get_payload(data):
    payload = ""
    for key, value in data.items():
        payload += f"{key}={value}&"
    payload = payload.encode("utf-8")
    return payload


def get_user_data(base_path, user_id):
    url = f"{base_path}{user_id}?key={API_KEY_GET}"
    response = requests.request("GET", url, headers={}, data={})
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


def get_full_user_data(base_url, timestamp, per_page=1000):
    url = f"{base_url}?key={API_KEY_GET}&per_page={per_page}&activity_after={timestamp}&group=126"
    response = requests.request("GET", url, headers={}, data={})
    json = response.json()
    return json["results"]


def calculate_level(base_url, member):
    custom_fields = member["customFields"]
    raw_user_data = dict()
    for raw in custom_fields.values():
        raw_user_data.update(raw["fields"])
    user_data = dict()
    for key, value in raw_user_data.items():
        user_data.update({key: value["value"]})

    forum_id = member["id"]
    posts = float(member["posts"]) * 5
    galleons = float(user_data["12"]) * 0.2 if user_data["12"] != "" else 0

    object_points = float(user_data["34"]) * 25 if user_data["34"] != "" else 0
    creatures_points = float(user_data["33"]) * 25 if user_data["33"] != "" else 0

    knowledge_number = float(user_data["41"]) * 4000 if user_data["41"] != "" else 0
    skill_number = float(user_data["42"]) * 12000 if user_data["42"] != "" else 0
    power_number = float(user_data["63"]) * 6000 if user_data["63"] != "" else 0

    dungeon_points = float(user_data["71"]) * 2500 if user_data["71"] != "" else 0
    set_points = float(user_data["11"]) * 1220 if user_data["11"] != "" else 0

    badget_points = float(user_data["60"]) if user_data["60"] != "" else 0

    # New Values
    posts = 50000 if posts > 50000 else posts
    galleons = 80000 if galleons > 80000 else galleons

    object_points = 75000 if object_points > 75000 else object_points
    creatures_points = 75000 if creatures_points > 75000 else creatures_points

    knowledge_number = 96000 if knowledge_number > 96000 else knowledge_number
    skill_number = 132000 if skill_number > 132000 else skill_number
    power_number = 60000 if power_number > 60000 else power_number

    dungeon_points = 62500 if dungeon_points > 62500 else dungeon_points
    set_points = 120000 if set_points > 120000 else set_points

    experience = (
        round(posts, 2)
        + round(galleons, 2)
        + round(object_points, 2)
        + round(creatures_points, 2)
        + round(knowledge_number, 2)
        + round(skill_number, 2)
        + round(power_number, 2)
        + round(dungeon_points, 2)
        + round(set_points, 2)
        + round(badget_points, 2)
    )
    raw_level = experience / 10000
    level = int(round(raw_level, 0))
    payload = get_payload({"customFields[43]": f"{level}"})
    url = f"{base_url}{forum_id}?key={API_KEY_POST}"
    response = post_request(url, payload)
    return response
