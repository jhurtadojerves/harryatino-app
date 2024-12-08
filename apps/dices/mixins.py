import operator
from functools import reduce

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import FormView
from superadmin.templatetags.superadmin_utils import site_url

from apps.dices.forms import CustomDiceForm, RollForm
from apps.dices.models import Dice
from apps.dices.services import RollService
from apps.utils.services import TopicAPIService


class TopicFormMixin:
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.data = TopicAPIService.get_topic_data(self.object.topic_id)

        if self.action == "create":
            self.object.user = self.request.user

        self.object.save()

        return super().form_valid(form)


class TopicDetailMixin(FormView):
    form_class = RollForm
    second_form_class = CustomDiceForm

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data()
        rolls = self.object.rolls.all()
        page = self.request.GET.get("page", 1)
        paginator = Paginator(rolls, per_page=10)

        if int(page) > paginator.num_pages:
            page = paginator.num_pages

        current_page = paginator.page(page)
        context.update(
            {
                "rolls": paginator,
                "current_page": current_page,
                "is_paginated": True,
                "page": page,
                "default_form": self.second_form_class(topic_id=self.object.id),
            }
        )

        return context

    def get(self, request, *args, **kwargs):
        """Validate user and login"""
        self.object = self.get_object()
        roll = request.GET.get("roll", False)

        if roll:
            context = self.get_context_data()
            url_page = request.GET.get("page", False)

            for pg in context["rolls"]:
                ids = [r.id for r in pg.object_list]

                if int(roll) in ids:
                    page_roll = pg.number

                    if not url_page or int(url_page) != page_roll:
                        redirect_url = site_url(self.object, "detail")
                        redirect_url += f"?page={page_roll}&roll={roll}#roll{roll}"

                        return redirect(redirect_url)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        dice = None
        self.object = self.get_object()

        if not self.object.dice_is_available:
            messages.error(request, "No tienes permisos para realizar esta acción 🥲")
            return redirect(site_url(self.object, "detail"))

        sides = int(request.POST.get("sides", 0))
        number = int(request.POST.get("number", 0))
        modifier = request.POST.get("modifier", False)
        modifier_value = request.POST.get("modifier_value", 0)
        result_operation = request.POST.get("result_operation", False)
        default_dice = request.POST.get("dice", False)

        if not self.object.allow_custom and not default_dice:
            messages.error(
                request, "No se permite enviar dados personalizados en este topic"
            )
            return redirect(site_url(self.object, "detail"))

        if default_dice:
            form = self.get_form(self.second_form_class)
            dice = Dice.objects.get(id=default_dice)
            (
                sides,
                number,
                modifier,
                result_operation,
                modifier_value,
            ) = dice.get_values()

            if not dice.categories.filter(id=self.object.category.id).exists():
                messages.error(
                    request,
                    "Por favor actualiza la página y vuelve a lanzar",
                )

                return redirect(site_url(self.object, "detail"))

        else:
            form = self.get_form()

        if not form.is_valid():
            messages.error(request, "No se pudo lanzar el dado, intentalo nuevamente")
            return self.form_invalid(form)

        result, numeric_result = RollService.roll_dice(
            sides=sides,
            number=number,
            modifier=modifier,
            modifier_value=modifier_value,
            result_operation=result_operation,
        )

        roll = form.save(commit=False)
        roll.topic = self.object
        roll.user = request.user
        roll.result = result
        roll.numeric_result = numeric_result

        if dice:
            roll.road_message = dice.get_road_message(
                roll.numeric_result, roll.user.profile.clean_nick()
            )

        roll.save()

        message = ""
        if roll.numeric_result is not None:
            message = roll.road_message

        response, html = TopicAPIService.create_post(
            topic=self.object.topic_id,
            context={
                "nick": roll.user.profile.clean_nick(),
                "result": roll.result,
                "url": f"{self.object.detail_url}?roll={roll.id}",
                "message": message,
            },
            template="dices/posts/dice.html",
        )

        roll.post_url = response.get("url")
        roll.save(update_fields=["post_url"])

        url = site_url(self.object, "detail")
        full_url = f"{url}?&roll={roll.id}"

        return redirect(full_url)


class DiceMixin:
    def form_valid(self, form):
        self.object = form.save(commit=False)
        configuration = self.request.POST.dict()
        configuration.pop("csrfmiddlewaretoken")
        self.object.configuration = configuration
        self.object.save()

        return super().form_valid(form)


class TopicListMixin:
    def get_queryset(self):
        search_params_config = (
            "data__title__icontains",
            "data__author__name__icontains",
            "topic_id__icontains",
        )
        queryset = super().get_queryset().order_by("-state", "created_date")
        search_params = self.request.GET

        if search_params:
            params = search_params.dict()
            search = params.pop("search", None)
            params.pop("page", None)
            params.pop("paginate_by", None)
            search = (
                (search.replace("+", ",").replace(";", ",")).split(",")
                if search
                else None
            )

            if search:
                for search_value in search:
                    filters = {
                        key: search_value.strip() for key in search_params_config
                    }
                    params.update(**filters)
                    args = [Q(**{key: value}) for key, value in filters.items()]
                    queryset = queryset.filter(reduce(operator.__or__, args))

        return queryset
