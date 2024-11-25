from django.contrib import messages
from django.shortcuts import redirect
from superadmin.templatetags.superadmin_utils import site_url

from apps.management.models import LevelUpdate
from apps.management.services import LevelUpdateService


class LevelUpdateMixin:
    def get(self, request, *args, **kwargs):
        previous_updates = LevelUpdate.objects.filter(state=LevelUpdate.workflow.DRAFT)

        if previous_updates:
            first = previous_updates.first()

            messages.info(
                request, "Ya existe un proceso de actualización de niveles en curso"
            )

            return redirect(site_url(first, "detail"))

        new_level_update = LevelUpdate.objects.create()
        LevelUpdateService.create_lines(new_level_update)

        return redirect(site_url(new_level_update, "detail"))
