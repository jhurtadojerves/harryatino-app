"""Views to custom forms"""
# Python
from datetime import datetime
import time

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
        custom_fields = data["customFields"]
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


class UpdateLevelsForm(BaseForm):
    """Get data for update levels"""

    social_ranks = {
        "0": "Aprendiz",
        "1": "Unicornios de Bronce",
        "2": "Unicornios de Bronce",
        "3": "Unicornios de Plata",
        "4": "Unicornios de Plata",
        "5": "Unicornios de Oro",
        "6": "Unicornios de Oro",
        "7": "Dragones de Bronce",
        "8": "Dragones de Bronce",
        "9": "Dragones de Bronce",
        "10": "Dragones de Plata",
        "11": "Dragones de Plata",
        "12": "Dragones de Plata",
        "13": "Dragones de Plata",
        "14": "Dragones de Plata",
        "15": "Dragones de Oro",
        "16": "Dragones de Oro",
        "17": "Dragones de Oro",
        "18": "Dragones de Oro",
        "19": "Dragones de Oro",
        "20": "Orden de la Cruz Dorada",
        "21": "Orden de la Cruz Dorada",
        "22": "Orden de la Cruz Dorada",
        "23": "Orden de la Cruz Dorada",
        "24": "Orden de la Cruz Dorada",
        "25": "Orden de la Cruz Dorada",
        "26": "Orden de la Cruz Dorada",
        "27": "Orden de la Cruz Dorada",
        "28": "Orden de la Cruz Dorada",
        "29": "Orden de la Cruz Dorada",
        "30": "Orden del Caduceo",
        "31": "Orden del Caduceo",
        "32": "Orden del Caduceo",
        "33": "Orden del Caduceo",
        "34": "Orden del Caduceo",
        "35": "Orden del Caduceo",
        "36": "Orden del Caduceo",
        "37": "Orden del Caduceo",
        "38": "Orden del Caduceo",
        "39": "Orden del Caduceo",
        "40": "Orden del Grial",
        "41": "Orden del Grial",
        "42": "Orden del Grial",
        "43": "Orden del Grial",
        "44": "Orden del Grial",
        "45": "Orden del Grial",
        "46": "Orden del Grial",
        "47": "Orden del Grial",
        "48": "Orden del Grial",
        "49": "Orden del Grial",
        "50": "Supremo Consejo de Morgana",
        "51": "Supremo Consejo de Morgana",
        "52": "Supremo Consejo de Morgana",
        "53": "Supremo Consejo de Morgana",
        "54": "Supremo Consejo de Morgana",
        "55": "Supremo Consejo de Morgana",
        "56": "Supremo Consejo de Morgana",
        "57": "Supremo Consejo de Morgana",
        "58": "Supremo Consejo de Morgana",
        "59": "Supremo Consejo de Morgana",
        "60": "Supremo Consejo de Circe",
        "61": "Supremo Consejo de Circe",
        "62": "Supremo Consejo de Circe",
        "63": "Supremo Consejo de Circe",
        "64": "Supremo Consejo de Circe",
        "65": "Supremo Consejo de Circe",
        "66": "Supremo Consejo de Circe",
        "67": "Supremo Consejo de Circe",
        "68": "Supremo Consejo de Circe",
        "69": "Supremo Consejo de Circe",
        "70": "Supremo Consejo de Hécate",
        "71": "Supremo Consejo de Hécate",
        "72": "Supremo Consejo de Hécate",
        "73": "Supremo Consejo de Hécate",
        "74": "Supremo Consejo de Hécate",
        "75": "Supremo Consejo de Hécate",
        "76": "Supremo Consejo de Hécate",
        "77": "Supremo Consejo de Hécate",
        "78": "Supremo Consejo de Hécate",
        "79": "Supremo Consejo de Hécate",
        "80": "Orden de Merlín",
    }

    def get(self, request, *args, **kwargs):
        try:
            now = datetime.now()
            previous_date = now.replace(day=1, month=now.month - 3)
            timestamp = datetime.timestamp(previous_date)
            members = self.get_full_user_data(self.BASE_API_URL, timestamp)
            members_data = list()
            for member in members:
                """print(member)
                data = self.calculate_level(self.BASE_API_URL, member)
                if data:
                    members_data.append(data)"""
                try:
                    data = self.calculate_level(self.BASE_API_URL, member)
                    if data:
                        members_data.append(data)
                except Exception as e:
                    print(member)

            AuditAPI.objects.create(
                username=request.user, data=members_data, action="Niveles actualizados"
            )
            return JsonResponse({"status": 200, "message": "Niveles actualizados"})
        except ValueError:
            return JsonResponse({}, status=500)

    def calculate_level(self, base_url, member):
        custom_fields = member["customFields"]
        raw_user_data = dict()
        for raw in custom_fields.values():
            raw_user_data.update(raw["fields"])
        user_data = dict()
        for key, value in raw_user_data.items():
            user_data.update({key: value["value"]})

        forum_id = member["id"]
        # posts = float(member["posts"]) * 5
        old_posts = user_data["39"]
        new_posts = float(member["posts"])
        posts = (
            int(old_posts) * 5
            if (old_posts and old_posts != "" and int(old_posts) >= new_posts)
            else new_posts * 5
        )
        galleons = (
            float(user_data["12"]) * 0.2
            if (user_data["12"] and user_data["12"] != "")
            else 0
        )
        object_points = (
            float(user_data["34"]) * 25
            if (user_data["34"] and user_data["34"] != "")
            else 0
        )

        creatures_points = (
            float(user_data["33"]) * 25
            if (user_data["33"] and user_data["33"] != "")
            else 0
        )

        knowledge_number = (
            float(user_data["41"]) * 4000
            if (user_data["41"] and user_data["41"] != "")
            else 0
        )

        skill_number = (
            float(user_data["42"]) * 12000
            if (user_data["42"] and user_data["42"] != "")
            else 0
        )
        power_number = (
            float(user_data["63"]) * 6000
            if (user_data["63"] and user_data["63"] != "")
            else 0
        )

        dungeon_points = (
            float(user_data["71"]) * 25
            if (user_data["71"] and user_data["71"] != "")
            else 0
        )
        set_points = (
            float(user_data["11"]) * 1220
            if (user_data["11"] and user_data["11"] != "")
            else 0
        )

        badget_points = (
            float(user_data["60"]) if (user_data["60"] and user_data["60"] != "") else 0
        )

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
            posts
            + galleons
            + object_points
            + creatures_points
            + knowledge_number
            + skill_number
            + power_number
            + dungeon_points
            + set_points
            + badget_points
        )
        raw_level = experience / 10000
        level = int(round(raw_level, 0))
        url = f"{base_url}{forum_id}?key={API_KEY_POST}"
        actual_level = user_data["43"]
        organization = (
            119249,
            119247,
            119248,
            119738,
            119739,
            119246,
            119242,
            119769,
            119772,
            119781,
            119773,
            119770,
            119768,
        )

        if member["id"] in organization:
            level = 80
        actual_level = int(actual_level) if actual_level and actual_level != "" else 0
        graduate = user_data["40"] if user_data["40"] else ""
        if graduate == "Graduado":
            social_rank = self.social_ranks[f"{level}"]
        else:
            social_rank = "Aprendiz"
        payload_data = {
            "customFields[43]": f"{level}",
            "customFields[61]": f"{social_rank}",
        }

        # if ,
        range_team = self.get_range_team(user_data["76"])
        if range_team:
            payload_data.update({"customFields[22]": range_team})
        payload = self.get_payload(payload_data)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()
        response = {
            "user": {
                "id": data["id"],
                "nick": data["name"],
                "old_level": actual_level,
                "calculated_value": level,
                "social_rank": social_rank,
            },
            "action": "updated",
        }
        return response

    @staticmethod
    def get_full_user_data(base_url, timestamp, per_page=1000):
        url = f"{base_url}?key={API_KEY_GET}&perPage={per_page}&activity_after={timestamp}"
        # &group=126 this key can be used to filter by id group
        response = requests.request("GET", url, headers={}, data={})
        json = response.json()
        return json["results"]

    @staticmethod
    def get_range_team(team, level, inactive):
        # ID customFieldsInactive => 76
        # ID customFieldsRange => 22
        if inactive and inactive == "Inactivo":
            return "Sin rango por inactividad"
        if not team or not level:
            return ""
        if team == "Orden del Fénix":
            if 1 <= level <= 9:
                return "Initie"
            elif 10 <= level <= 21:
                return "Legionario"
            elif 22 <= level <= 36:
                return "Templario"
            elif 37 <= level <= 55:
                return "Knight"
            # elif 56 <= level <= 60:
            else:
                return "Demon Hunter"
        if team == "Marca Tenebrosa":
            if 1 <= level <= 9:
                return "Base"
            elif 10 <= level <= 21:
                return "Tempestad"
            elif 22 <= level <= 36:
                return "Mago Oscuro"
            elif 37 <= level <= 55:
                return "Nigromante"
            # elif 56 <= level <= 60:
            else:
                return "Ángel Caído"


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


"""
    def fix(self):
        pass
        # Fix Poderes

        poderes = ["62"]
        fix_poderes = {
            "Libro del Aprendiz de Brujo (N.1)": 1,
            "Libro de la Fortaleza (N.5)": 2,
            "Libro de la Sangre (N.7)": 3,
            "Libro del Equilibrio (N.10)": 4,
            "Libro del Druida (N.15)": 5,
            "Libro del Caos (N.20)": 6,
            "Libro de los Ancestros (N.25)": 7,
            "Libro de las Auras (N.30)": 8,
            "Libro de Hermes Trimegisto (N.35)": 9,
            "Libro de Merlín (N.40)": 10,
        }
        numero_poderes = fix_poderes.get(poderes, 0)
        payload = self.get_payload({"customFields[63]": f"{numero_poderes}"})
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        url = f"{base_url}{forum_id}?key={API_KEY_POST}"
        response = requests.request("POST", url, headers=headers, data=payload)
return 1"""
