"""Define services to profile"""

# Python
import time
import re

# Third party integration
from environs import Env
import requests

env = Env()

API_KEY_GET = env("API_KEY")

# Local
from apps.payments.models import Work


class BaseService:
    POSTS_GET_URL = "https://www.harrylatino.org/api/forums/posts"

    @classmethod
    def get_posts(cls, authors, per_page=1000, page=1):
        url = cls.get_url(authors, page, per_page)
        response = requests.request("GET", url, headers={}, data={})
        json = response.json()
        results = json["results"]
        total_pages = int(json["totalPages"])
        print(f"{page} de {total_pages}")
        if total_pages != page:
            return results + cls.get_posts(authors, per_page, page=page + 1)
        return results

    @classmethod
    def get_url(cls, authors, page, per_page):
        return f"{cls.POSTS_GET_URL}?key={API_KEY_GET}&page={page}&perPage={per_page}&forums=510&authors={authors}&sortBy=date&sortDir=desc"


class ProfileService(BaseService):
    @staticmethod
    def get_profiles_id(works):
        authors = list(works.values_list("wizard__forum_user_id", flat=True))
        authors = map(str, authors)
        authors = ",".join(authors)
        return authors

    @classmethod
    def calculate_member_posts(cls, month, works, per_page=500):
        authors = cls.get_profiles_id(works)
        monthly_posts = get_profiles(authors)
        total_posts = get_profiles(authors)
        posts = cls.get_posts(authors, per_page)
        first_day = time.strptime(month.first_day(), "%Y-%m-%dT%H:%M:%SZ")
        last_day = time.strptime(month.last_day(), "%Y-%m-%dT%H:%M:%SZ")
        for post in posts:
            author = post["author"]  # Get author object
            author_id = author["id"]  # Get author id
            post_date = post["date"]  # Get post date
            python_post_date = time.strptime(
                post_date, "%Y-%m-%dT%H:%M:%SZ"
            )  # Create python time
            total_value = total_posts.get(f"{author_id}", list())
            total_value.append(post["date"])
            total_posts.update({f"{author_id}": total_value})
            if first_day <= python_post_date <= last_day:
                monthly_value = monthly_posts.get(f"{author_id}", list())
                monthly_value.append(post["date"])
                monthly_posts.update({f"{author_id}": monthly_value})
        return total_posts, monthly_posts


class PropertyService(BaseService):
    POSTS_GET_URL = "https://www.harrylatino.org/api/forums/topics/"

    # {id}/posts
    @classmethod
    def get_url(cls, topic_id, page, per_page):
        return f"{cls.POSTS_GET_URL}{topic_id}/posts/?key={API_KEY_GET}&page={page}&perPage={per_page}&sortBy=date&sortDir=desc"

    @classmethod
    def calculate_property_posts(cls, payment, topic_id, per_page=500):
        posts = cls.get_posts(topic_id, per_page)
        first_day = time.strptime(payment.first_day(), "%Y-%m-%dT%H:%M:%SZ")
        last_day = time.strptime(payment.last_day(), "%Y-%m-%dT%H:%M:%SZ")
        monthly_posts = list()
        for post in posts:
            post_date = post["date"]  # Get post date
            python_post_date = time.strptime(
                post_date, "%Y-%m-%dT%H:%M:%SZ"
            )  # Create python time
            if first_day <= python_post_date <= last_day:
                monthly_posts.append(post)

        return monthly_posts

    @classmethod
    def previous_value_in_vault(cls, payment):
        vault = payment.property.vault
        url = f"{cls.POSTS_GET_URL}{vault}?key={API_KEY_GET}"
        response = requests.request("GET", url, headers={}, data={})
        json = response.json()
        last_post = json["lastPost"]
        last_post_content = last_post["content"]
        galleons = re.findall(
            r"Total en Bóveda:\s(?P<galleons>\d*)\sG", last_post_content
        )
        if galleons:
            galleons = int(galleons[0])
        else:
            galleons = re.findall(r"Saldo:\s(?P<galleons>\d*)\sG", last_post_content)
            galleons = int(galleons[0]) if galleons else 0
        return galleons

    @classmethod
    def get_posts(cls, authors, per_page=1000, page=1):
        url = cls.get_url(authors, page, per_page)
        response = requests.request("GET", url, headers={}, data={})
        json = response.json()
        results = json["results"]
        total_pages = int(json["totalPages"])
        if total_pages != page:
            return results + cls.get_posts(authors, per_page, page=page + 1)
        return results


def get_profiles(authors):
    authors = authors.split(",")
    author_dictionary = {}
    for author in authors:
        author_dictionary.update({author: list()})
    return author_dictionary