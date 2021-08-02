"""Define views urls"""

import re

# Django
from django.views.generic import DetailView
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.http import JsonResponse

# Local
from .service import ProfileService, PropertyService
from apps.payments.models import (
    MonthPayment,
    MonthPaymentLine,
    Work,
    PropertyPayment,
    PropertyPaymentLine,
)
from apps.properties.models import Property
from apps.dynamicforms.views import UpdateTopicsForm, UpdateProfileForm
from apps.dynamicforms.views import API_KEY

# Third party integration
import requests
from superadmin.templatetags.superadmin_utils import site_url


class CalculatePaymentPropertyView(DetailView):
    model = PropertyPayment

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        properties = Property.objects.filter(
            property_type=self.object.payment_type, is_active=True
        )
        lines = list()
        for p in properties:
            posts = len(PropertyService.calculate_property_posts(self.object, p.rol))
            galleons = self.calculate_payment(posts)
            if galleons > 0:
                lines.append(
                    PropertyPaymentLine(
                        payment=self.object, property=p, posts=posts, galleons=galleons
                    )
                )
        PropertyPaymentLine.objects.bulk_create(lines)
        return redirect(site_url(self.object, "detail"))

    @staticmethod
    def calculate_payment(quantity):
        multiplier = 0
        if 1 <= quantity <= 5:
            multiplier = 75
        elif 6 <= quantity <= 10:
            multiplier = 100
        elif 11 <= quantity <= 15:
            multiplier = 125
        elif quantity > 15:
            multiplier = 150
        return quantity * multiplier


class CalculatePaymentView(DetailView):
    model = MonthPayment

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        works = Work.objects.filter(is_active=True)
        total, monthly = ProfileService.calculate_member_posts(self.object, works)
        for key, value in total.items():
            work = works.filter(wizard__forum_user_id=key).get()
            if work.wizard.accumulated_posts != len(value):
                work.wizard.accumulated_posts = len(value)
                work.wizard.salary_scale = work.wizard.calculate_salary_scale()
                work.wizard.save()

        for key, value in monthly.items():
            work = works.filter(wizard__forum_user_id=key).get()
            number_of_posts = len(value)
            if number_of_posts >= 5:
                calculated_value = work.wizard.calculate_payment_value()
                MonthPaymentLine.objects.update_or_create(
                    work=work,
                    month=self.object,
                    defaults={
                        "number_of_posts": number_of_posts,
                        "calculated_value": calculated_value,
                    },
                )
            profile = work.wizard
            salary_scale = profile.salary_scale
            accumulated_posts = profile.accumulated_posts
            data = self.get_payload(
                {
                    "customFields[74]": f"{salary_scale}",
                    "customFields[73]": f"{accumulated_posts}",
                    "customFields[31]": f"{number_of_posts}",
                }
            )
            self.update_galleons_in_profile(
                data,
                profile.forum_user_id,
                UpdateProfileForm.URL,
            )
        return redirect(site_url(self.object, "detail"))

    @staticmethod
    def update_galleons_in_profile(data, user_id, url):
        url = f"{url}{user_id}?key={API_KEY}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request("POST", url, headers=headers, data=data)
        return response.json()

    @staticmethod
    def get_payload(data):
        payload = ""
        for key, value in data.items():
            payload += f"{key}={value}&"
        payload = payload.encode("utf-8")
        return payload


class CreatePaymentView(DetailView):
    model = MonthPaymentLine
    template_name = "payments/cmi.html"
    update_title_url = "https://www.harrylatino.org/api/forums/topics/"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.paid:
            return JsonResponse(
                {
                    "status_code": 403,
                    "message": "El deposito ya fue realizado anteriormente",
                    "url": self.object.paid_url,
                }
            )
        if not self.object.work.post_url:
            if self.object.paid:
                return JsonResponse(
                    {
                        "status_code": 403,
                        "message": "Debes configurar el link del post de petición",
                        "url": False,
                    }
                )
        try:
            profile = self.object.work.wizard
            salary_scale = profile.salary_scale
            accumulated_posts = profile.accumulated_posts
            number_of_posts = self.object.number_of_posts
            data = UpdateProfileForm.get_data(
                UpdateProfileForm.URL, profile.forum_user_id
            )[0]
            previous_galleons = data.get("customFields[12]", False)
            previous_galleons = int(previous_galleons) if previous_galleons else 0
            galleons = self.object.calculated_value
            total_galleons = galleons + previous_galleons
            response_post = self.create_post(
                request, previous_galleons, profile.vault_number
            )
            data = self.get_payload(
                {
                    "customFields[12]": f"{total_galleons}",
                    "customFields[74]": f"{salary_scale}",
                    "customFields[73]": f"{accumulated_posts}",
                    "customFields[31]": f"{number_of_posts}",
                }
            )
            response_profile = self.update_galleons_in_profile(
                data,
                profile.forum_user_id,
                UpdateProfileForm.URL,
            )
            self.object.paid_url = response_post["url"]
            self.object.paid = True
            self.object.save()
            return JsonResponse(
                {"status_code": 200, "message": "Deposito realizado correctamente"}
            )

        except Exception as e:
            return {"status_code": 500, "message": str(e)}

    @staticmethod
    def update_galleons_in_profile(data, user_id, url):
        url = f"{url}{user_id}?key={API_KEY}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request("POST", url, headers=headers, data=data)
        return response.json()

    def post_html(self, data={}):
        return render_to_string(self.template_name, context=data)

    def create_post(self, request, previous_galleons, topic):
        galleons = self.object.calculated_value
        html = self.post_html(
            data={
                "previous_galleons": previous_galleons,
                "url": self.object.work.post_url,
                "reason": f"CMI {self.object.month.__str__()}",
                "galleons": galleons,
                "total_galleons": galleons + previous_galleons,
            },
        )
        author = request.user.profile.forum_user_id
        payload = f"topic={topic}&author={author}&post={html}"
        url = f"https://www.harrylatino.org/api/forums/posts?key={API_KEY}"
        response = self.post_request(url, payload)
        return response.json()

    def update_vault_title(self, vault, title):
        url = f"https://www.harrylatino.org/api/forums/topics/{vault}/?key={API_KEY}"
        data = self.get_payload({"title": title})
        return self.post_request(url, data)

    @staticmethod
    def get_payload(data):
        payload = ""
        for key, value in data.items():
            payload += f"{key}={value}&"
        payload = payload.encode("utf-8")
        return payload

    @staticmethod
    def post_request(url, payload):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response


class CreatePaymentPropertyView(CreatePaymentView):
    model = PropertyPaymentLine
    template_name = "payments/properties.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.paid:
            return JsonResponse(
                {
                    "status_code": 403,
                    "message": "El deposito ya fue realizado anteriormente",
                    "url": self.object.paid_url,
                }
            )
        try:
            previous_galleons = PropertyService.previous_value_in_vault(self.object)
            galleons = self.object.galleons
            if self.object.property.property_type == 0:
                reason = f"Familias {self.object.payment.__str__()}"
            else:
                reason = f"Negocios {self.object.payment.__str__()}"
            response_post = self.create_post(
                request,
                {
                    "previous_galleons": previous_galleons,
                    "url": "#",
                    "reason": reason,
                    "galleons": galleons,
                    "total_galleons": galleons + previous_galleons,
                },
                self.object.property.vault,
            )
            self.object.paid_url = response_post["url"]
            self.object.paid = True
            self.object.save()
            return JsonResponse(
                {"status_code": 200, "message": "Depósito realizado correctamente"}
            )
        except Exception as e:
            return {"status_code": 500, "message": str(e)}

    def create_post(self, request, data, topic):

        html = self.post_html(data)
        author = request.user.profile.forum_user_id
        payload = f"topic={topic}&author={author}&post={html}"
        url = f"https://www.harrylatino.org/api/forums/posts?key={API_KEY}"
        response = self.post_request(url, payload)
        return response.json()
