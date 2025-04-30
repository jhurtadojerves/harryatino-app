from django.db import models
from tracing.models import BaseModel


class TopicAPI(BaseModel):
    key = models.CharField(verbose_name="Clave", unique=True, max_length=32)
    topic_id = models.PositiveIntegerField(verbose_name="Id del topic")
    description = models.CharField(
        verbose_name="Detalle de donde se usará el id", max_length=128, default=""
    )

    def save(self, *args, **kwargs):
        from apps.utils.services import TopicAPIService

        TopicAPIService.clean_cache(self.key, self.topic_id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.key} - {self.topic_id}"
