import ast
import json

from django import forms
from django.apps import apps

from .utils import items_attr


# Create your views here.
class FieldDynamic(object):
    """
    Class define Field Dynamic add import custom fields initial file
    * from .fields import MyChoiceField, MySelect2Widget
    """

    CLASS_CUSTOM_TYPE = ["MyChoiceField"]
    CLASS_CUSTOM_WIDGET = ["MySelect2Widget"]
    OPERATOR_SPLIT = ","

    def __init__(
        self,
        label,
        required=False,
        attrs_widget=None,
        class_type=None,
        class_widget=None,
        disabled=False,
    ):
        self.label = label
        self.required = required
        self.attrs_widget = attrs_widget
        self.class_type = class_type
        self.class_widget = class_widget
        self.model = self.get_model()
        self.queryset = self.get_queryset()
        self.default = {"data-placeholder": "Seleccione un elemento"}
        self.disabled = disabled

    def clean_attrs_widget(self):
        return items_attr(self.attrs_widget)

    def get_item_attrs_widget(self, item):
        attrs = self.clean_attrs_widget()
        return attrs.get(item, None)

    def get_model(self):
        model = self.get_item_attrs_widget("model")
        if model:
            try:
                app_label, model_name = model.split(".")
                model = apps.get_model(app_label, model_name)
            except ValueError:
                model = model
            return model
        return model

    def get_queryset(self):
        if self.model:
            return self.model.objects.all()
        return None

    def get_kwargs_class_type(self):
        kwargs = {
            "label": self.label,
            "required": self.required,
            "disabled": self.disabled,
        }
        if self.queryset:
            kwargs.update({"queryset": self.queryset})
        choices = self.get_item_attrs_widget("choices")
        if choices:
            choices = ast.literal_eval(choices)
            kwargs.update({"choices": choices})
        return kwargs

    def get_kwargs_class_widget(self):
        kwargs = {}
        if self.model:
            kwargs.update({"model": self.model})
        search_fields = self.get_item_attrs_widget("search_fields")
        if search_fields:
            search_fields = search_fields.split(self.OPERATOR_SPLIT)
            search_fields = [item.strip() for item in search_fields]
            kwargs.update({"search_fields": search_fields})
        choices = self.get_item_attrs_widget("choices")
        if choices:
            choices = ast.literal_eval(choices)
            kwargs.update({"choices": choices})
        attrs = self.get_item_attrs_widget("attrs")
        if attrs:
            attrs = json.loads(attrs)
            if self.model:
                attrs.update(self.default)
            kwargs.update({"attrs": attrs})
        return kwargs

    @property
    def create_field(self):
        class_form = None
        if self.class_type in self.CLASS_CUSTOM_TYPE:
            class_form = eval(self.class_type)
        elif hasattr(forms, self.class_type):
            class_form = getattr(forms, self.class_type)
        if class_form:
            class_form = class_form(**self.get_kwargs_class_type())
            if self.create_widget:
                class_form.widget = self.create_widget
            return class_form
        return class_form

    @property
    def create_widget(self):
        class_widget = None
        if self.class_widget:
            if self.class_widget in self.CLASS_CUSTOM_WIDGET:
                class_widget = eval(self.class_widget)
            elif hasattr(forms, self.class_widget):
                class_widget = getattr(forms, self.class_widget)
        if class_widget:
            return class_widget(**self.get_kwargs_class_widget())
        return class_widget
