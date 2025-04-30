import re
import time
from datetime import datetime, timedelta
from typing import Optional

import requests
from django.contrib import messages
from django.db.models import Sum
from django.template.loader import render_to_string
from environs import Env
from superadmin.templatetags.superadmin_utils import site_url

from apps.utils.services import LinkService, TopicAPIService, UserAPIService
from apps.workflows.exceptions import WorkflowException

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


class DonationService:
    from apps.payments.models.donations import Donation, DonationLine

    USER_LIMIT_DONATION = 8000
    LINES_LIMIT = 2
    TOPIC_PARTIAL_URL = "https://harrylatino.org/index.php?showtopic="
    REQUEST_TOPIC_ID = 121051
    VAULT_USER_ID = 121976
    REQUEST_TOPIC_KET = "donations"

    @classmethod
    def confirm(cls, donation: Donation):
        giver = donation.user.profile
        UserAPIService.update_user_profile_v2(giver)
        cls.validate_galleons(donation)

        html = render_to_string(
            context=cls.get_context_for_request(donation),
            template_name="payments/posts/donations/request.html",
        )
        response = TopicAPIService.create_post_v2(
            topic=TopicAPIService.get_topic_id(key_id=cls.REQUEST_TOPIC_KET),
            html=html,
            author=giver.forum_user_id,
        )
        donation.request_html = html
        donation.request_url = response.get("url")
        donation.save()

    @classmethod
    def approve(cls, donation: Donation):
        giver = donation.user.profile
        UserAPIService.update_user_profile_v2(giver)
        cls.validate_galleons(donation)

        # Create donation lines posts
        for line in donation.lines.all():
            cls.donate(line)

        html = render_to_string(
            context=cls.get_context_for_giver(donation),
            template_name="payments/posts/donations/minus.html",
        )
        # Create donation post
        response = TopicAPIService.create_post_v2(
            topic=giver.vault_number,
            html=html,
            author=cls.VAULT_USER_ID,
        )

        donation.vault_html = html
        donation.vault_discount_url = response.get("url")
        donation.save()

        galleons = giver.galleons - donation.total
        update_profile_data = {
            "customFields[12]": str(galleons),
        }
        giver.galleons = galleons
        giver.save()
        UserAPIService.update_user_profile(
            giver.forum_user_id, raw_data=update_profile_data
        )

    @classmethod
    def donate(cls, line: DonationLine):
        beneficiary = line.beneficiary
        UserAPIService.update_user_profile_v2(beneficiary)
        context = cls.get_context_for_line(line)
        html = render_to_string(
            context=context,
            template_name="payments/posts/donations/plus.html",
        )
        response = TopicAPIService.create_post_v2(
            topic=beneficiary.vault_number,
            html=html,
            author=cls.VAULT_USER_ID,
        )
        line.vault_html = html
        line.vault_deposit_url = response.get("url")
        line.save()

        galleons = str(context["galleons"]["new"])
        update_profile_data = {
            "customFields[12]": galleons,
        }
        beneficiary.galleons = galleons
        beneficiary.save()

        UserAPIService.update_user_profile(
            beneficiary.forum_user_id, raw_data=update_profile_data
        )

    @classmethod
    def get_context_for_request(cls, donation: Donation) -> dict:
        giver = donation.user.profile
        raw_lines = donation.lines.all()
        lines = []

        for line in raw_lines:
            beneficiary = line.beneficiary
            UserAPIService.update_user_profile_v2(beneficiary)
            lines.append(
                {
                    "beneficiary": {
                        "nick": beneficiary.clean_nick(),
                        "profile_url": beneficiary.profile_url,
                        "vault_url": f"{cls.TOPIC_PARTIAL_URL}{beneficiary.vault_number}",
                        "vault_number": beneficiary.vault_number,
                    },
                    "quantity": line.quantity,
                    "reason": line.reason or "--",
                }
            )

        data = {
            "giver": {
                "nick": giver.clean_nick(),
                "profile_url": giver.profile_url,
                "vault_url": f"{cls.TOPIC_PARTIAL_URL}{giver.vault_number}",
                "vault_number": giver.vault_number,
            },
            "donation": {
                "total": donation.total,
                "lines": lines,
                "detail_url": donation.detail_url,
                "id": donation.id,
            },
        }

        return data

    @classmethod
    def get_context_for_line(cls, line: DonationLine):
        donation = line.donation
        giver = donation.user.profile
        beneficiary = line.beneficiary

        data = {
            "galleons": {
                "old": beneficiary.galleons,
                "new": int(beneficiary.galleons + line.quantity),
            },
            "giver": {"nick": giver.clean_nick()},
            "line": {"quantity": line.quantity},
            "donation": {
                "request_url": LinkService.get_resolved_short_url(donation.request_url),
                "created_date": donation.created_date,
            },
        }

        return data

    @classmethod
    def get_context_for_giver(cls, donation: Donation):
        galleons = donation.user.profile.galleons
        lines = []

        for line in donation.lines.all():
            lines.append(
                {
                    "vault_deposit_url": LinkService.get_resolved_short_url(
                        line.vault_deposit_url
                    ),
                    "quantity": line.quantity,
                    "beneficiary": {"nick": line.beneficiary.clean_nick()},
                }
            )

        data = {
            "galleons": {"old": galleons, "new": int(galleons - donation.total)},
            "donation": {
                "request_url": LinkService.get_resolved_short_url(donation.request_url),
                "created_date": donation.created_date,
                "total": donation.total,
            },
            "lines": lines,
        }

        return data

    @classmethod
    def get_redirect(cls, request) -> Optional[str]:
        from apps.payments.models.donations import Donation

        created_donations = Donation.objects.filter(
            state__in=[
                Donation.workflow.CREATED.value,
                Donation.workflow.CONFIRMED.value,
            ],
            user=request.user,
        )

        if created_donations:
            messages.info(request, "Tienes una donación en curso")

            return site_url(created_donations.last(), "detail")

    @classmethod
    def validate_donation(cls, request):
        from apps.payments.models.donations import Donation

        thirty_days_ago = datetime.now() - timedelta(days=30)
        other_donations = Donation.objects.filter(
            confirm_date__gte=thirty_days_ago,
            state=Donation.workflow.APPROVED.value,
            user=request.user,
        )

        if other_donations:
            raise WorkflowException(
                f"Ya realizaste una donación el {other_donations.last().confirm_date}"
            )

    @classmethod
    def validate_line(cls, line: DonationLine):
        from apps.payments.models.donations import DonationLine

        thirty_days_ago = datetime.now() - timedelta(days=30)
        other_lines = DonationLine.objects.filter(
            donation__confirm_date__gte=thirty_days_ago,
            beneficiary=line.beneficiary,
            donation__state__in=[2, 3],
        )

        if other_lines:
            quantity_sum = (
                other_lines.aggregate(total_quantity=Sum("quantity")).get(
                    "total_quantity", 0
                )
                or 0
            ) + line.quantity

            if quantity_sum > cls.USER_LIMIT_DONATION:
                raise WorkflowException(
                    f"Superaste el monto de galeones que puedes recibir este mes ({cls.USER_LIMIT_DONATION})"
                )

    @classmethod
    def validate_edit_line(cls, line: DonationLine):
        from apps.payments.models.donations import DonationLine

        thirty_days_ago = datetime.now() - timedelta(days=30)
        other_lines = DonationLine.objects.filter(
            donation__confirm_date__gte=thirty_days_ago,
            beneficiary=line.beneficiary,
            donation__state__in=[2, 3],
        ).exclude(id=line.pk)

        if other_lines:
            quantity_sum = (
                other_lines.aggregate(total_quantity=Sum("quantity")).get(
                    "total_quantity", 0
                )
                or 0
            ) + line.quantity

            if quantity_sum > cls.USER_LIMIT_DONATION:
                raise WorkflowException(
                    f"Superaste el monto de galeones que puedes recibir este mes ({cls.USER_LIMIT_DONATION})"
                )

    @classmethod
    def not_is_full(cls, donation: Donation):
        if donation.is_full():
            raise WorkflowException(
                f"Solo puedes donar a {donation.MAX_LINES} usuarios"
            )

    @classmethod
    def validate_galleons(cls, donation: Donation):
        if donation.total > donation.user.profile.galleons:
            raise WorkflowException(
                "La bóveda tienes los galeones suficientes para realizar esta donación"
            )
