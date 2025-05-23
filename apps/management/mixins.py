from django.contrib import messages
from django.shortcuts import redirect
from superadmin.templatetags.superadmin_utils import site_url

from apps.dynamicforms.models import Form
from apps.dynamicforms.services import FormService
from apps.management.models import LevelUpdate
from apps.management.services import LevelUpdateService, ProfileHistoryService


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


class ProfileHistoryDetailMixin:
    form_id = 7

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data()
        form = Form.objects.filter(id=self.form_id).first()
        form_service = FormService(self.request, form)
        original_data = self.object.original_data
        new_data = self.object.new_data
        original_template = form_service.get_form(
            data=original_data, disable_fields=True
        )
        new_template = form_service.get_form(data=new_data or {}, disable_fields=True)
        changes = self.get_changes(original_data, new_data)
        context.update(
            {
                "original_template": original_template,
                "new_template": new_template,
                "changes": changes,
            }
        )

        return context

    def get_changes(self, original_data, new_data):
        return {
            ProfileHistoryService.get_field_name(k): (
                {"original_data": original_data.get(k), "new_data": new_data[k]}
            )
            for k in new_data
            if original_data.get(k) != new_data[k]
        }


class EntryHistoryDetailMixin:
    form_id = 6

    def get_changes(self, original_data, new_data):
        original_data.pop("author", None)
        original_data.pop("title", None)
        new_data.pop("author", None)
        new_data.pop("title", None)
        return {
            k: ({"original_data": original_data.get(k), "new_data": new_data[k]})
            for k in new_data
            if original_data.get(k) != new_data[k]
        }

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data()
        original_data = self.object.original_data
        new_data = self.object.new_data
        changes = self.get_changes(original_data, new_data)
        context.update({"changes": changes})

        return context
