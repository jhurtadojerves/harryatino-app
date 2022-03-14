"""Custom views for model"""
# Django
from django.urls import reverse_lazy

# Local
from .forms import SaleConsumableUsedForm
from apps.sales.models import Sale
from apps.insoles.views import InstanceBaseFormView


class UseConsumableFormView(InstanceBaseFormView):
    model = Sale
    form_class = SaleConsumableUsedForm
    create_url_name = "sales_sale_consumable_form"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.available = False
        instance.save()
        return self.success("Formulario guardado éxito.")
