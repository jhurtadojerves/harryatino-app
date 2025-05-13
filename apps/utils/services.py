"""Services from utils module"""

# Third party integration
from typing import Optional

import requests
from django.conf import settings
from django.template.loader import render_to_string
from environs import Env
from pydantic import BaseModel, ValidationError
from superadmin.templatetags.superadmin_utils import site_url

# Models
from apps.profiles.models.profiles import Profile
from apps.utils.cache import CacheService
from apps.utils.classes.profile import ForumProfile
from apps.utils.decorators import cache_decorator
from apps.utils.models import Link

env = Env()
API_KEY = env("API_KEY")
API_KEY_MP = env("API_KEY_MP")
API_KEY_GET = env("API_KEY")
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
        return f"{settings.SITE_URL.geturl()}{url}"


class APIService:
    @classmethod
    def get_payload(cls, data):
        payload = ""

        for key, value in data.items():
            payload += f"{key}={value}&"

        payload = payload.encode("utf-8")

        return payload

    @classmethod
    def post(cls, url, payload):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()


class UserAPIService(APIService):
    USER_API_URL = "https://www.harrylatino.org/api/core/members/"

    @classmethod
    def send_personal_message(cls, to_users_id: list, title, body, from_user_id=121976):
        cleaned_to = ",".join(to_users_id)
        payload = cls.get_payload(
            {"from": from_user_id, "title": title, "body": body, "to[]": cleaned_to}
        )
        url = f"{PERSONAL_MESSAGE_API_URL}?key={API_KEY_MP}"

        return cls.post(url, payload)

    @classmethod
    def update_user_profile(cls, user_id, raw_data):
        payload = cls.get_payload(raw_data)
        url = f"{cls.USER_API_URL}{user_id}?key={API_KEY}"
        return cls.post(url, payload)

    @classmethod
    def download_user_data_and_update(cls, wizard: Profile) -> Profile:
        profile_data, nick = cls.get_forum_user_data(wizard=wizard, get_nick_name=True)
        wizard.range_of_creatures = profile_data.get("customFields[35]", "")
        wizard.range_of_objects = profile_data.get("customFields[36]", "")
        wizard.galleons = int(profile_data.get("customFields[12]", "") or 0)
        wizard.magic_level = int(profile_data.get("customFields[43]", "") or 0)
        wizard.nick = nick
        wizard.formatted_name = profile_data.get("formatted_name")
        boxroom_number = profile_data.get("customFields[66]", 75080)
        vault_number = profile_data.get("customFields[64]", None)
        character_sheet = profile_data.get("customFields[65]", None)

        if boxroom_number:
            wizard.boxroom_number = int(boxroom_number)

        if vault_number:
            wizard.vault_number = int(vault_number)

        if character_sheet:
            wizard.character_sheet = int(character_sheet)

        avatar = profile_data.get("avatar")

        if len(avatar) <= 512:
            wizard.avatar = avatar

        wizard.save()
        wizard = Profile.objects.get(pk=wizard.pk)

        return wizard

    @classmethod
    def get_forum_user_data(cls, wizard, get_nick_name=False):
        url = f"{cls.USER_API_URL}{wizard.forum_user_id}?key={API_KEY}"
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()
        custom_fields = data.get("customFields", False)
        raw_user_data = dict()
        user_data = dict()

        if not custom_fields:
            return dict()

        for raw in custom_fields.values():
            raw_user_data.update(raw["fields"])

        for key, value in raw_user_data.items():
            user_data.update({f"customFields[{key}]": value["value"]})

        user_data.update(
            {
                "avatar": data.get("photoUrl", ""),
                "formatted_name": data.get("formattedName", ""),
                "nick": data.get("name"),
            }
        )

        if get_nick_name:
            return user_data, data.get("name")

        return user_data

    @classmethod
    def get_forum_user_data_v2(cls, wizard):
        url = f"{cls.USER_API_URL}{wizard.forum_user_id}?key={API_KEY}"
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()
        custom_fields = data.get("customFields", False)
        raw_user_data = dict()
        user_data = dict()

        for raw in custom_fields.values():
            raw_user_data.update(raw["fields"])

        for key, value in raw_user_data.items():
            user_data.update({f"customFields[{key}]": value["value"]})

        data.update(user_data)
        data.update(
            {"nick": data.get("name"), "formatted_name": data.get("formattedName")}
        )

        return data

    @classmethod
    def get_forum_user_data_v3(cls, forum_user_id):
        url = f"{cls.USER_API_URL}{forum_user_id}?key={API_KEY}"
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()
        custom_fields = data.get("customFields", False)
        raw_user_data = dict()
        user_data = dict()

        for raw in custom_fields.values():
            raw_user_data.update(raw["fields"])

        for key, value in raw_user_data.items():
            user_data.update({f"customFields[{key}]": value["value"]})

        data.update(user_data)
        data.update(
            {"nick": data.get("name"), "formatted_name": data.get("formattedName")}
        )

        return data

    @classmethod
    def get_for_key(cls, data, key):
        return data.get(f"customFields[{key}]", "")

    @classmethod
    def get_multiple_users(cls, timestamp, per_page=1000):
        url = (
            f"{cls.USER_API_URL}?key={API_KEY_GET}&perPage={per_page}"
            f"&activity_after={timestamp}"
        )
        # &group=126 this key can be used to filter by id group
        response = requests.request("GET", url, headers={}, data={})
        json = response.json()

        return json["results"]

    @classmethod
    def download_user_data(cls, wizard) -> ForumProfile:
        data = cls.get_forum_user_data_v2(wizard)

        return ForumProfile(**data)

    @classmethod
    def update_user_profile_v2(cls, wizard) -> Optional[str]:
        try:
            profile = cls.download_user_data(wizard)
        except Exception as error:
            return cls.format_pydantic_errors(error, ForumProfile)

        wizard.range_of_creatures = profile.creatures
        wizard.range_of_objects = profile.objects
        wizard.galleons = profile.galleons
        wizard.magic_level = profile.level
        wizard.nick = profile.nick
        wizard.formatted_name = profile.formatted_name
        wizard.boxroom_number = profile.boxroom_number
        wizard.vault_number = profile.vault
        wizard.character_sheet = profile.character
        wizard.profile_url = profile.profile_url
        wizard.save()

    @classmethod
    def get_updated_profile_data(cls, forum_user_id):
        try:
            data = cls.get_forum_user_data_v3(forum_user_id)

            return ForumProfile(**data), None
        except Exception as error:
            return None, cls.format_pydantic_errors(error, ForumProfile)

    @classmethod
    def format_pydantic_errors(cls, error: ValidationError, model: BaseModel):
        field_map = {field.alias: name for name, field in model.model_fields.items()}
        messages = []

        for err in error.errors():
            field_alias = err["loc"][0]
            field_name = field_map.get(field_alias, field_alias)
            message = err["msg"]
            messages.append(cls.translate(f"Error en {field_name}: {message}"))

        return "\n".join(messages)

    @classmethod
    def translate(cls, message):
        MESSAGES = {
            "Error en vault: Input should be a valid integer, unable to parse string as an integer": "La bóveda es obligatoria"
        }

        return MESSAGES.get(message, message)


class TopicAPIService(APIService):
    CREATE_POST_API_URL = f"https://www.harrylatino.org/api/forums/posts?key={API_KEY}"
    GET_TOPIC_URL = "https://www.harrylatino.org/api/forums/topics/"
    TOPIC_ID_CACHE_KEY = "topic_id"
    DEFAULT_AUTHOR = 121976

    @classmethod
    def create_post(cls, topic, context, template, author=121976):
        html = render_to_string(context=context, template_name=template)
        payload = cls.get_payload({"topic": topic, "author": author, "post": html})

        if settings.MOCK_CREATE_POST:
            data = {
                "url": "https://www.harrylatino.org/forums/topic/119285-pruebas-generales/?do=findComment&comment=5517357"
            }
        else:
            data = cls.post(url=cls.CREATE_POST_API_URL, payload=payload)

        return data, html

    @classmethod
    def get_topic_data(cls, topic_id):
        url = f"{cls.GET_TOPIC_URL}{topic_id}/?key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        first_post = data.get("firstPost", {})

        return {
            "id": data.get("id"),
            "title": data.get("title"),
            "content": first_post.get("content"),
            "author": first_post.get("author", {}),
            "date": first_post.get("date"),
        }

    @classmethod
    def create_custom_post(cls, date, topic, html="...", author=121976):
        payload = cls.get_payload(
            {"topic": topic, "author": author, "post": html, "date": date}
        )
        data = cls.post(url=cls.CREATE_POST_API_URL, payload=payload)

        return data

    @classmethod
    def create_post_v2(cls, topic: int, html: str, author: int):
        payload = cls.get_payload({"topic": topic, "author": author, "post": html})

        return cls.post(url=cls.CREATE_POST_API_URL, payload=payload)

    @cache_decorator(TOPIC_ID_CACHE_KEY, ["key_id"])
    @classmethod
    def get_topic_id(cls, key_id):
        from apps.utils.models.api import TopicAPI

        try:
            topic = TopicAPI.objects.get(key=key_id)
            return topic.topic_id
        except TopicAPI.DoesNotExist:
            return None

    @classmethod
    def clean_cache(cls, key_id, value):
        cache_id = CacheService.generate_cache_key(
            cls.TOPIC_ID_CACHE_KEY, ["key_id"], key_id=key_id
        )
        CacheService.set_cache(
            cache_id,
            value,
        )
