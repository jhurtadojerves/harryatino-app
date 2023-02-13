"""Define services to profile"""

import re

# Python
import time

import requests
from environs import Env

# Third party integration
from superadmin.templatetags.superadmin_utils import site_url

from apps.utils.services import UserAPIService

env = Env()
API_KEY = env("API_KEY")
API_KEY_GET = env("API_KEY")


class BaseService:
    POSTS_GET_URL = "https://www.harrylatino.org/api/forums/posts"

    @classmethod
    def get_posts(cls, authors=(), per_page=1000, page=1):
        url = cls.get_url(authors, page, per_page)
        response = requests.request("GET", url, headers={}, data={})
        json = response.json()
        results = json["results"]
        total_pages = int(json["totalPages"])
        print(f"{page} de {total_pages}")

        if total_pages != page and total_pages > 0:
            return results + cls.get_posts(authors, per_page, page=page + 1)

        return results

    @classmethod
    def get_url(cls, authors, page, per_page):
        url = (
            f"{cls.POSTS_GET_URL}?key={API_KEY_GET}&page={page}&perPage={per_page}"
            f"&forums=510&sortBy=date&sortDir=desc"
        )
        if authors:
            url = f"{url}&authors={authors}"
        return url

    @classmethod
    def calculate_all_posts(cls, posts):
        author_posts = {}
        for post in posts:
            data = author_posts.get(
                post["author"]["id"], {"nick": post["author"]["name"], "data": list()}
            )
            data["data"].append({"url": post["url"], "date": post["date"]})
            author_posts.update({post["author"]["id"]: data})
        return author_posts


class MonthlyPaymentService(BaseService):
    @staticmethod
    def get_profiles_id(works):
        authors = list(works.values_list("wizard__forum_user_id", flat=True))
        authors = map(str, authors)
        authors = ",".join(authors)
        return authors

    @classmethod
    def calculate_member_posts(cls, month, work):

        authors = f"{work.wizard.forum_user_id}"
        monthly_posts = cls.get_profiles(authors)
        total_posts = cls.get_profiles(authors)
        first_day = time.strptime(month.first_day(), "%Y-%m-%dT%H:%M:%SZ")
        last_day = time.strptime(month.last_day(), "%Y-%m-%dT%H:%M:%SZ")
        posts = BaseService.get_posts(authors=authors, per_page=1000)

        author = {}

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

        custom_fields = author.get("customFields", {})
        data_raw = custom_fields.get("3", {}).get("fields", {})
        galleons = data_raw.get("12", {}).get("value", 0)
        galleons = int(galleons) if galleons else 0

        return total_posts.get(authors, []), monthly_posts.get(authors, []), galleons

    @classmethod
    def calculate_payment(cls, line, posts, galleons):
        work = line.work
        profile = work.wizard
        number_of_posts = len(posts)
        profile.refresh_from_db()

        calculated_value = 0

        if number_of_posts >= 5:
            calculated_value = profile.calculate_payment_value()
            line.number_of_posts = number_of_posts
            line.calculated_value = calculated_value

        salary_scale = profile.salary_scale
        accumulated_posts = profile.accumulated_posts
        data = {
            "customFields[74]": f"{salary_scale}",
            "customFields[73]": f"{accumulated_posts}",
            "customFields[31]": f"{number_of_posts}",
            "customFields[12]": f"{galleons + calculated_value}",
        }
        UserAPIService.update_user_profile(profile.forum_user_id, data)

        return calculated_value

    @classmethod
    def get_profiles(cls, authors):
        authors = authors.split(",")
        author_dictionary = {}

        for author in authors:
            author_dictionary.update({author: list()})

        return author_dictionary

    @classmethod
    def calculate_salary_scale(cls, line, posts):
        profile = line.work.wizard

        if profile.accumulated_posts != len(posts):
            profile.accumulated_posts = len(posts)
            profile.salary_scale = profile.calculate_salary_scale()
            profile.save(update_fields=["accumulated_posts", "salary_scale"])


class PropertyService(BaseService):
    POSTS_GET_URL = "https://www.harrylatino.org/api/forums/topics/"

    # {id}/posts
    @classmethod
    def get_url(cls, topic_id, page, per_page):
        return (
            f"{cls.POSTS_GET_URL}{topic_id}/posts/?key={API_KEY_GET}&page={page}"
            f"&perPage={per_page}&sortBy=date&sortDir=desc"
        )

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


class PaymentService:
    from apps.sales.models import Sale

    @classmethod
    def get_or_create_payment_for_sale(cls, sale: Sale):
        from apps.payments.models import Payment, PaymentLine

        sale_url = f"https://magicmall.rol-hl.com{site_url(sale, 'detail')}"
        payment, created = Payment.objects.get_or_create(
            state=1, wizard=sale.profile, payment_type=0
        )
        PaymentLine.objects.create(
            payment=payment,
            amount=sale.product.cost,
            verbose=sale.product.name,
            link=sale_url,
        )

        return payment
