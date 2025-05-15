import time

import requests
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView
from environs import Env

from apps.dynamicforms.forms import CreationDynamicForm

from .models import Action, AuditAPI

env = Env()
API_KEY_GET = env("API_KEY_GET")
API_KEY_POST = env("API_KEY_POST")
API_KEY = env("API_KEY")
IGNORE_OLD_LEVE = env.bool("IGNORE_OLD_LEVE", False)


class MixinDynamicForm:
    """Mixin form create dynamic form"""

    METHOD_ACCEPT = ["POST", "PUT"]

    def _get_form_kwargs(self, attr, data=dict):
        kwargs = {"initial": data}
        if self.request.method in self.METHOD_ACCEPT:
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
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

    def post_request(self, request, api_key, payload_function):
        data = request.POST.dict()
        user_id = request.GET.get("user_id", False)
        url = f"{self.URL}{user_id}?key={api_key}"
        del data["csrfmiddlewaretoken"]
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload_function(data)
        )
        return self.get_response(
            request.user,
            response,
            data,
            user_id,
            "guardar",
            "Información actualizada",
        )

    @staticmethod
    def get_response(user, response, data, user_id, action, message):
        if response.status_code == 200:
            data = {"data": data, "user_id": user_id}
            AuditAPI.objects.create(username=user, data=data, action=action)
            return JsonResponse({"status": 200, "message": message})
        else:
            return JsonResponse({"status": 403, "message": "Sucedió un error"})

    def get_form(self, user_id):
        attr = {"form": self.object.form}
        data, username = self.get_data(self.BASE_API_URL, user_id)
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

    @staticmethod
    def get_payload(data):
        payload = ""
        for key, value in data.items():
            payload += f"{key}={value}&"
        payload = payload.encode("utf-8")
        return payload


class UpdateProfileForm(BaseForm):
    URL = "https://www.harrylatino.org/api/core/members/"

    def post(self, request, *args, **kwargs):
        return self.post_request(request, API_KEY_POST, self.get_payload)

    @staticmethod
    def get_data(api_url, user_id):
        url = f"{api_url}{user_id}?key={API_KEY_GET}"
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()
        custom_fields = data.get("customFields", False)
        if not custom_fields:
            return False, False
        raw_user_data = dict()
        for raw in custom_fields.values():
            raw_user_data.update(raw["fields"])
        username = data["name"]
        user_data = dict()
        for key, value in raw_user_data.items():
            user_data.update({f"customFields[{key}]": value["value"]})
        return user_data, username


class UpdateTopicsForm(BaseForm):
    """Get data for update levels"""

    BASE_API_URL = "https://www.harrylatino.org/api/forums/topics/"
    URL = BASE_API_URL

    @staticmethod
    def get_data(api_url, topic_id):
        url = f"{api_url}{topic_id}?key={API_KEY}"
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()
        return data, ""

    def post(self, request, *args, **kwargs):
        return self.post_request(request, API_KEY_POST, self.get_payload)


class UpdatePostForm(UpdateTopicsForm):
    BASE_API_URL = "https://www.harrylatino.org/api/forums/posts/"
    URL = "https://www.harrylatino.org/api/forums/posts/"

    @staticmethod
    def get_data(api_url, topic_id):
        url = f"{api_url}{topic_id}?key=a558a350a81d71e06a6d0ae449d9d773"
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()
        return data, ""

    def post(self, request, *args, **kwargs):
        return self.post_request(
            request, "a558a350a81d71e06a6d0ae449d9d773", self.get_payload
        )


class CountMonthlyPostsForm(BaseForm):
    """Count the monthly post in topic"""

    BASE_API_URL = "https://www.harrylatino.org/api/forums/topics/"
    URL = BASE_API_URL

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.GET.get("user_id")
            initial_date = request.GET.get("initial_date")
            end_date = request.GET.get("end_date")
            self.object = self.get_object()
            form, username, data = self.get_form(user_id, initial_date, end_date)
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

    def get_form(self, user_id, initial_date, end_date):
        attr = {"form": self.object.form}
        data, username = self.get_data(
            self.BASE_API_URL, user_id, initial_date, end_date
        )
        form = self._get_form(self.form_class, attr, data)
        return form, username, data

    def post(self, request, *args, **kwargs):
        return self.post_request(request, API_KEY_POST, self.get_payload)

    def get_data(self, api_url, topic_id, initial_date, end_date):
        url = f"{api_url}{topic_id}/posts?perPage=2000&key={API_KEY}"
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()
        return {
            "number_of_posts": self.check_date(data["results"], initial_date, end_date)
        }, ""

    def check_date(self, posts, initial_date, end_date):
        initial_date = time.strptime(initial_date, "%Y-%m-%d")
        end_date = time.strptime(end_date, "%Y-%m-%d")
        in_date_posts = list()
        for post in posts:
            post_date = time.strptime(post["date"], "%Y-%m-%dT%H:%M:%SZ")
            if initial_date <= post_date <= end_date:
                in_date_posts.append(post)
        return len(in_date_posts)
