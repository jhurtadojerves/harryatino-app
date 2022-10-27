from django.forms import inlineformset_factory

from apps.dynamicforms.forms import FieldLineForm
from apps.dynamicforms.models import Field, Form

FieldLineFormset = inlineformset_factory(
    Form,
    Field,
    form=FieldLineForm,
    min_num=0,
    validate_min=False,
)
