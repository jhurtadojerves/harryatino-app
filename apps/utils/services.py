"""Services from utils module"""

# Third party integration
import requests
from django.template.loader import render_to_string
from environs import Env
from superadmin.templatetags.superadmin_utils import site_url

# Models
from apps.utils.models import Link

env = Env()
API_KEY = env("API_KEY")
API_KEY_MP = env("API_KEY_MP")
PERSONAL_MESSAGE_API_URL = "https://www.harrylatino.org/api/core/messages"
# params:
"""
from int   User ID conversation is from
to array One or more user IDs conversation is sent to
title  string Conversation title
body string Conversation body
"""


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
    def get_payload_personal_message(cls, data, user_to):
        payload = ""
        for key, value in data.items():
            payload += f"{key}={value}&"
        payload += user_to
        payload = payload.encode("utf-8")
        return payload

    @classmethod
    def save_forum_user_data(cls, wizard):
        data = {}
        url = f"{cls.USER_BASE_URL}{wizard.forum_user_id}?key={API_KEY}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        requests.request("POST", url, headers=headers, data=cls.get_payload(data))

    @classmethod
    def get_forum_user_data(cls, wizard, get_nick_name=False):
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

        if get_nick_name:
            return user_data, data.get("name")

        return user_data

    @classmethod
    def create_post(cls, topic, context, template, author=121976):
        html = render_to_string(context=context, template_name=template)
        payload = f"topic={topic}&author={author}&post={html}"
        url = f"https://www.harrylatino.org/api/forums/posts?key={API_KEY}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=iso-8859-1",
        }
        response = requests.post(url, headers=headers, data=payload)
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

    @classmethod
    def send_personal_message(cls, to_users_id, title, body, from_user_id=121976):
        payload = cls.get_payload_personal_message(
            {"from": from_user_id, "title": title, "body": body}, to_users_id
        )
        url = f"{PERSONAL_MESSAGE_API_URL}?key={API_KEY_MP}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    @classmethod
    def download_user_data_and_update(cls, wizard):
        profile_data, nick = cls.get_forum_user_data(wizard=wizard, get_nick_name=True)
        wizard.range_of_creatures = profile_data.get("customFields[35]", "")
        wizard.range_of_objects = profile_data.get("customFields[36]", "")
        wizard.galleons = int(profile_data.get("customFields[12]", 0))
        boxroom_number = profile_data.get("customFields[66]", None)
        vault_number = profile_data.get("customFields[64]", None)
        character_sheet = profile_data.get("customFields[65]", None)

        if boxroom_number:
            wizard.boxroom_number = int(boxroom_number)

        if vault_number:
            wizard.vault_number = int(vault_number)

        if character_sheet:
            wizard.character_sheet = int(character_sheet)

        wizard.save()
        wizard.refresh_from_db()

        return wizard

    @classmethod
    def get_for_key(cls, data, key):
        return data.get(f"customFields[{key}]", "")
