# Django
from django.urls import path

# Views
from .views import ShowForm

urlpatterns = [
    path(
        route="dynamicforms/data/<int:pk>/", view=ShowForm.as_view(), name="data_url",
    ),
]
