"""Define services to profile"""

# Python
import time

# Third party integration
from environs import Env
import requests

env = Env()

API_KEY_GET = env("API_KEY")

# Local
from apps.payments.models import Work


class ProfileService:
    POSTS_GET_URL = "https://www.harrylatino.org/api/forums/posts"

    @classmethod
    def get_posts(cls, authors, per_page=1000, page=1):
        url = f"{cls.POSTS_GET_URL}?key={API_KEY_GET}&page={page}&perPage={per_page}&forums=510&authors={authors}&sortBy=date&sortDir=desc"
        response = requests.request("GET", url, headers={}, data={})
        json = response.json()
        results = json["results"]
        total_pages = int(json["totalPages"])
        if total_pages != page:
            return results + cls.get_posts(authors, per_page, page=page + 1)
        return results

    @staticmethod
    def get_profiles_id(works):
        authors = list(works.values_list("wizard__forum_user_id", flat=True))
        authors = map(str, authors)
        authors = ",".join(authors)
        return authors

    @classmethod
    def calculate_member_posts(cls, month, works, per_page=1000):
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


def get_profiles(authors):
    authors = authors.split(",")
    author_dictionary = {}
    for author in authors:
        author_dictionary.update({author: list()})
    return author_dictionary
