from django.template.loader import render_to_string

from apps.dynamicforms.forms import CreationDynamicForm
from apps.dynamicforms.models import Form


class FormService:
    METHOD_ACCEPT = ["POST", "PUT"]
    TEMPLATE_NAME = "insoles/form.html"
    form_class = CreationDynamicForm

    def __init__(self, request, form: Form):
        self.form = form
        self.request = request

    def get_form(self, data, disable_fields=False):
        attr = {"form": self.form}
        form = self._get_form(
            self.form_class, attr, data, disable_fields=disable_fields
        )
        template = render_to_string(self.TEMPLATE_NAME, context={"form": form})

        return template

    def _get_form_kwargs(self, attr, data=dict, disable_fields: bool = False):
        kwargs = {"initial": data, "disable_fields": disable_fields}
        kwargs.update(**attr)

        if self.request.method in self.METHOD_ACCEPT:
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )

        return kwargs

    def _get_form(self, form_class, attr, data, disable_fields=False):
        return form_class(**self._get_form_kwargs(attr, data, disable_fields))
