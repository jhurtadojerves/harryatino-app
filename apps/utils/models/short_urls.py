"""Define models to short urls"""
# Python
import uuid

# Django
from django.db import models
from django.urls import reverse

# Third Party Integration Models
from ckeditor.fields import RichTextField

# Models
from tracing.models import BaseModel


class Link(BaseModel):
    token = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    destination = models.URLField(
        null=True, blank=False, editable=False, unique=True, db_index=True
    )

    def __str__(self):
        return self.destination

    class Meta(BaseModel.Meta):
        verbose_name = "link"
        verbose_name_plural = "links"
