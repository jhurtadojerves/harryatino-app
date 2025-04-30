from django.contrib import admin

from apps.utils.models.api import TopicAPI


@admin.register(TopicAPI)
class TopicAPIAdmin(admin.ModelAdmin):
    pass
