"""Custom fields"""
# django
from django.core import validators
from django.db.models import Q
from django.forms import ChoiceField

# Third party integration
from django_select2.forms import ModelSelect2Widget


class MyChoiceField(ChoiceField):
    """Overwrite class custom ChoiceField"""

    def __init__(self, *, choices=(), queryset, to_field_name=None, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
        self.queryset = queryset
        self.to_field_name = to_field_name

    def valid_value(self, value):
        """Check to see if the provided value is a valid choice."""
        key = self.to_field_name or "pk"
        value = self.queryset.filter(**{key: value})
        if value.exists():
            return True
        return False


class MySelect2Widget(ModelSelect2Widget):
    """Overwrite Widget select2"""

    def optgroups(self, name, value, attrs=None):
        self.queryset = self.get_queryset()
        default = (None, [], 0)
        groups = [default]
        has_selected = False
        selected_choices = {str(v) for v in value}
        selected_choices = {
            c for c in selected_choices if c not in validators.EMPTY_VALUES
        }
        query = Q(**{"pk__in": selected_choices})
        for obj in self.queryset.filter(query):
            option_value = obj.pk
            option_label = self.label_from_instance(obj)
            selected = str(option_value) in value and (
                has_selected is False or self.allow_multiple_selected
            )
            if selected is True and has_selected is False:
                has_selected = True
            index = len(default[1])
            subgroup = default[1]
            subgroup.append(
                self.create_option(
                    name, option_value, option_label, selected_choices, index
                )
            )
        return groups
