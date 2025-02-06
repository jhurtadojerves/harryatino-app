# Django
from django.core.management import call_command
from django.core.management.base import BaseCommand

# Third party integration
from superadmin import site
from superadmin.models import Action, Menu

# Models
from apps.menu.models import Menu as PublicMenu


class Command(BaseCommand):
    help = "Create base menu mapping all apps"

    def handle(self, *args, **options):
        call_command("createactions")
        Menu.objects.all().delete()
        default_action = Action.objects.get(
            app_label="superadmin", element="ModuleView"
        )

        apps = {}
        for model in site._registry:
            if model._meta.app_config in apps:
                apps[model._meta.app_config].append(model)
            else:
                apps[model._meta.app_config] = [model]

        for app in apps:
            sequence = app.menu_sequence
            menu = Menu.objects.create(
                name=app.verbose_name.capitalize(),
                action=default_action,
                is_group=True,
                sequence=sequence,
            )

            index = 1
            for model in apps[app]:
                action = Action.objects.get(
                    app_label=app.label, element=model._meta.model_name
                )

                superadmin_menu = Menu.objects.create(
                    parent=menu,
                    name=model._meta.verbose_name_plural.capitalize(),
                    action=action,
                    is_group=False,
                    sequence=index,
                )
                local_site = site.get_modelsite(model)
                if hasattr(local_site, "menu_is_public") and local_site.menu_is_public:
                    PublicMenu.objects.get_or_create(public=superadmin_menu)
                index += 1

        self.stdout.write(self.style.SUCCESS("Successfully base menu was created"))
