"""Services from utils module"""

# Third party integration
from django.template.loader import render_to_string
from superadmin.templatetags.superadmin_utils import site_url
from environs import Env
import requests


# Models
from apps.utils.models import Link

env = Env()
API_KEY = env("API_KEY")


class LinkService:
    @classmethod
    def get_short_url(cls, destination):
        link, created = Link.objects.get_or_create(destination=destination)
        return link

    @classmethod
    def get_full_url(cls, token):
        return Link.objects.get(token=token).destination

    @classmethod
    def get_resolved_short_url(cls, link):
        instance = cls.get_short_url(link)
        url = site_url(instance, "detail")
        return f"https://magicmall.rol-hl.com{url}"


class APIService:
    USER_BASE_URL = "https://www.harrylatino.org/api/core/members/"

    @classmethod
    def get_payload(cls, data):
        payload = ""
        for key, value in data.items():
            payload += f"{key}={value}&"
        payload = payload.encode("utf-8")
        return payload

    @classmethod
    def save_forum_user_data(cls, wizard):
        data = {}
        url = f"{cls.USER_BASE_URL}{wizard.forum_user_id}?key={API_KEY}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request(
            "POST", url, headers=headers, data=cls.get_payload(data)
        )

    @classmethod
    def get_forum_user_data(cls, wizard):
        url = f"{cls.USER_BASE_URL}{wizard.forum_user_id}?key={API_KEY}"
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()
        custom_fields = data.get("customFields", False)
        if not custom_fields:
            return dict()
        raw_user_data = dict()
        for raw in custom_fields.values():
            raw_user_data.update(raw["fields"])
        user_data = dict()
        for key, value in raw_user_data.items():
            user_data.update({f"customFields[{key}]": value["value"]})
        return user_data

    @classmethod
    def create_post(cls, topic, context, template, author=0):
        html = render_to_string(context=context, template_name=template)
        if author == 0:
            author = 121976
        payload = f"topic={topic}&author={author}&post={html}"
        url = f"https://www.harrylatino.org/api/forums/posts?key={API_KEY}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json(), html

    @classmethod
    def update_user_profile(cls, user_id, raw_data):
        payload = cls.get_payload(raw_data)
        url = f"https://www.harrylatino.org/api/core/members/{user_id}?key={API_KEY}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
