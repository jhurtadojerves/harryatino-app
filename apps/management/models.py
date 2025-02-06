from datetime import datetime

from django.db import models
from django.db.models.functions import Lower
from django_fsm import FSMIntegerField
from tracing.models import BaseModel

from apps.management.transitions import (
    LevelUpdateLineTransitions,
    LevelUpdateTransitions,
)
from apps.profiles.models.profiles import Profile


class LevelUpdate(BaseModel, LevelUpdateTransitions):
    workflow = LevelUpdateTransitions.workflow
    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.DRAFT,
        protected=True,
        verbose_name="estado",
    )

    def __str__(self):
        fromated_created_date = datetime.strftime(
            self.created_date, "%d-%m-%Y %H:%M:%S"
        )
        return f"Actualización de niveles ({fromated_created_date})"

    @property
    def is_done(self):
        return self.state == self.workflow.DONE

    @property
    def ordered_lines(self):
        return (
            self.lines.select_related("profile")
            .all()
            .order_by("state", Lower("profile__nick"))
        )

    class Meta(BaseModel.Meta):
        verbose_name = "Actualización de Niveles"
        verbose_name_plural = "Actualizaciones de Niveles"
        permissions = (("can_update_levels", "Can update levels"),)
        ordering = ["-id"]


class LevelUpdateLine(BaseModel, LevelUpdateLineTransitions):
    workflow = LevelUpdateLineTransitions.workflow
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="update_lines"
    )
    level_update = models.ForeignKey(
        LevelUpdate, on_delete=models.CASCADE, related_name="lines"
    )
    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.DRAFT,
        protected=True,
        verbose_name="estado",
    )
    calculated_level = models.IntegerField(default=0)
    calculated_social_rank = models.CharField(max_length=128, default="")
    old_level = models.IntegerField(default=0)
    content = models.JSONField()

    @property
    def is_done(self):
        return self.level_update.is_done
