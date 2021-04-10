"""Views for products"""

# Django
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import Q

# Mixins
from apps.utils.mixins import FormsetMixin

# Views
from apps.utils.views import (
    GenericCreateView,
    GenericDetailView,
    GenericListView,
    GenericUpdateView,
)

# Models
from apps.products.models import Category, Product, Section, StockRequest

# Forms
from apps.products.forms import (
    StockRequestForm,
    StockFormset,
    ProductUpdateForm,
    ProductCreateForm,
)


class StockList(LoginRequiredMixin, GenericListView):
    """Stock Create View"""

    model = StockRequest
    context_object_name = "stocks"
    paginate_by = 20
    list_display = (
        "name",
        "forum_url",
    )
