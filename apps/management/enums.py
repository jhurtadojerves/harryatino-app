from django.db import models


class TypeEntryChoices(models.TextChoices):
    TOPIC = "topic", "Topic"
    POST = "post", "Post"
