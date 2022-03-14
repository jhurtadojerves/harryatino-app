"""View to response rendered templates """

# Django
from django.views.generic import View
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy
from django.apps import apps
from django.forms import modelform_factory
from django.contrib.admin.utils import flatten

# Third party integration
from superadmin import site
from superadmin.views.detail import DetailMixin


class RenderDetailMixin(DetailMixin):
    def __init__(self, instance, site_instance, model):
        self.object = instance
        self.site = site_instance
        self.model = model
        super().__init__()


class RenderFormView(View):
    """View to get record filtering by date"""

    http_method_names = ["get", "post"]

    def get_form_class(self, **kwargs):
        app_name = kwargs.get("app")
        model_name = kwargs.get("model")
        app = apps.get_app_config(app_name)
        model = app.get_model(model_name)
        model_site = site._registry[model]

        if hasattr(model_site, "insoles_form"):
            form_class = model_site.insoles_form
        elif model_site.form_class:
            form_class = model_site.form_class
        else:
            form_class = modelform_factory(model, fields=model_site.fields)
        return form_class

    def get(self, request, *args, **kwargs):
        app_name = kwargs.get("app")
        model_name = kwargs.get("model")
        perms = [
            f"{app_name.lower()}.add_{model_name.lower()}",
        ]
        if model_name.lower() == "taxpayer":
            perms.extend(
                [
                    f"{app_name.lower()}.add_naturaltaxpayer",
                    f"{app_name.lower()}.add_legaltaxpayer",
                ]
            )

        if not any([request.user.has_perm(perm) for perm in perms]):
            return HttpResponseForbidden()
        form_class = self.get_form_class(**kwargs)
        context = {
            "form": form_class(),
        }
        create_url = reverse_lazy("insoles_form", args=[app_name, model_name])
        template = render_to_string("insoles/form.html", context=context)
        res = {"create_url": create_url, "template": template, "app": app_name}

        return JsonResponse(res, status=200)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class(**kwargs)
        form = form_class(self.request.POST, self.request.FILES)

        if form.is_valid():
            instance = form.save()

        res = {
            "id": instance.id,
            "text": str(instance),
        }

        return JsonResponse(res, status=200)


class RenderFieldView(RenderFormView):
    """View to get record filtering by date"""

    http_method_names = [
        "get",
    ]

    def get(self, request, *args, **kwargs):
        app_name = kwargs.get("app")
        model_name = kwargs.get("model")
        field_name = kwargs.get("field")

        if not self.request.user.has_perm(f"{app_name}.change_{model_name}"):
            return HttpResponseForbidden()

        form_class = self.get_form_class(**kwargs)
        form = form_class()
        context = {"field": form[field_name]}
        template = render_to_string("insoles/field.html", context=context)
        res = {"template": template}

        return JsonResponse(res, status=200)


class RenderDetailView(View):
    http_method_names = [
        "get",
    ]

    @staticmethod
    def get_data(**kwargs):
        app_name = kwargs.get("app")
        model_name = kwargs.get("model")
        reverse_value = kwargs.get("slug")
        field = kwargs.get("field")
        search = {field: reverse_value}
        app = apps.get_app_config(app_name)
        model = app.get_model(model_name)
        instance = model.objects.filter(**search)
        if instance.exists():
            instance = instance.get()
        else:
            return None
        model_site = site._registry[model]
        detail = RenderDetailMixin(
            instance=instance, site_instance=model_site, model=model
        )
        return detail.get_results()

    def get(self, request, *args, **kwargs):
        flatten_results, results = self.get_data(**kwargs)
        context = {
            "results": results,
        }
        template = render_to_string("insoles/detail.html", context=context)
        res = {
            "template": template,
        }
        return JsonResponse(res, status=200)


class RenderEditView(View):

    http_method_names = ["get", "post"]

    def get_instance(self, **kwargs):
        app_name = kwargs.get("app")
        model_name = kwargs.get("model")
        reverse_value = kwargs.get("slug")
        field = kwargs.get("field")
        if model_name == "User":
            field = "username"
        search = {field: reverse_value}
        app = apps.get_app_config(app_name)
        model = app.get_model(model_name)
        instance = model.objects.filter(**search)
        if instance.exists():
            return instance.get()
        return False

    def get_form_class(self, **kwargs):
        app_name = kwargs.get("app")
        model_name = kwargs.get("model")
        app = apps.get_app_config(app_name)
        model = app.get_model(model_name)
        model_site = site._registry[model]

        if hasattr(model_site, "insoles_edit"):
            form_class = model_site.insoles_edit
        else:
            form_class = modelform_factory(model, fields=model_site.fields)
        return form_class

    def get(self, request, *args, **kwargs):
        app_name = kwargs.get("app")
        model_name = kwargs.get("model")
        perms = [
            f"{app_name.lower()}.add_{model_name.lower()}",
        ]
        if model_name.lower() == "taxpayer":
            perms.extend(
                [
                    f"{app_name.lower()}.add_naturaltaxpayer",
                    f"{app_name.lower()}.add_legaltaxpayer",
                ]
            )
        if not any([request.user.has_perm(perm) for perm in perms]):
            return HttpResponseForbidden()
        form_class = self.get_form_class(**kwargs)
        instance = self.get_instance(**kwargs)
        context = {
            "form": form_class(instance=instance),
        }
        create_url = reverse_lazy("insoles_form", args=[app_name, model_name])
        template = render_to_string("insoles/form.html", context=context)
        res = {"create_url": create_url, "template": template, "app": app_name}

        return JsonResponse(res, status=200)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class(**kwargs)
        instance = self.get_instance(**kwargs)
        form = form_class(self.request.POST, self.request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save()

        res = {
            "id": instance.id,
            "text": str(instance),
        }

        return JsonResponse(res, status=200)


class InstanceBaseFormView(View):
    model = None
    form_class = None
    template_name = "insoles/form.html"
    http_method_names = ["get", "post"]
    create_url_name = None

    def get_create_url(self):
        if not self.create_url_name:
            raise Exception("En enlace de creación no se encuentra configurado")
        kwargs = {key: value for key, value in self.kwargs.items()}
        url = reverse_lazy(str(self.create_url_name), kwargs={**kwargs})
        return url

    def get_object(self):
        pk = self.kwargs.get("pk")
        return self.model.objects.get(pk=pk)

    def get_kwargs(self):
        kwargs = {"instance": self.get_object()}
        if self.request.POST or self.request.FILES:
            kwargs.update({"data": self.request.POST, "files": self.request.FILES})
        return kwargs

    def get_form_kwargs(self):
        kwargs = {**self.get_kwargs()}
        return kwargs

    def get_form(self):
        if not self.form_class:
            raise Exception(f"La clase de formulario no se encuentra configurada")
        return self.form_class(**self.get_form_kwargs())

    def get_context(self, request, *args, **kwargs):
        ctx = {"form": self.get_form()}
        return ctx

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.error("No estás autorizado para realizar esta acción")
        try:
            context = self.get_context(request, *args, **kwargs)
            template = render_to_string(self.template_name, context=context)
            create_url = self.get_create_url()
            response = {"template": template, "create_url": create_url}
            return JsonResponse(response, status=200)
        except Exception as e:
            return self.error(str(e))

    def post(self, request, *args, **kwargs):
        try:
            form = self.get_form()
            if not form.is_valid():
                return self.form_invalid(form)
            return self.form_valid(form)
        except Exception as err:
            return self.error(str(err))

    def form_invalid(self, form):
        errors = {key: value for key, value in form.errors.items()}
        message = "Formulario invalido. Algunos campos en el formulario son requeridos"
        ctx = {"error": message, "errors": errors}
        return JsonResponse(ctx, status=400)

    def form_valid(self, form):
        form.save()
        return self.success("Formulario guardado éxito.")

    def success(self, message):
        response = {"message": message}
        return JsonResponse(response, status=200)

    def error(self, message):
        response = {"error": message}
        return JsonResponse(response, status=400)

    def has_permission(self):
        return True


class InstanceBaseFormsetView(InstanceBaseFormView):
    queryset = None
    model = None
    formset_class = None
    template_name = "insoles/form.html"
    http_method_names = ["get", "post"]

    def get_context(self, request, *args, **kwargs):
        ctx = {"formset": self.get_formset()}
        return ctx

    def post(self, request, *args, **kwargs):
        try:
            formset = self.get_formset()
            if not formset.is_valid():
                return self.form_invalid(formset)
            return self.form_valid(formset)
        except Exception as err:
            return self.error(str(err))

    def form_invalid(self, formset):
        errors = {
            f"{form.prefix}-{field}": value
            for form in formset
            for field, value in form.errors.items()
            if form.errors
        }
        message = "Formulario invalido. Algunos campos en el formulario son requeridos"
        ctx = {"error": message, "errors": errors}
        return JsonResponse(ctx, status=400)

    def get_formset_kwargs(self):
        kwargs = {**self.get_kwargs()}
        if self.queryset:
            kwargs.update({"queryset": self.queryset})
        return kwargs

    def get_formset(self):
        if not self.formset_class:
            raise Exception("No se encuentra configurado formset_class")
        formset = self.formset_class(**self.get_formset_kwargs())
        formset.headers = [
            field.label
            for field in formset.empty_form.visible_fields()
            if field.name in formset.form.Meta.fields
        ]
        return formset
