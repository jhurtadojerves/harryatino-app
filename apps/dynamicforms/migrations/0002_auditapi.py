# Generated by Django 3.2.2 on 2021-05-07 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dynamicforms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditAPI",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="fecha de creación"
                    ),
                ),
                (
                    "created_user",
                    models.CharField(
                        editable=False,
                        max_length=128,
                        null=True,
                        verbose_name="creado por",
                    ),
                ),
                (
                    "modified_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="última fecha de modificación"
                    ),
                ),
                (
                    "modified_user",
                    models.CharField(
                        editable=False,
                        max_length=128,
                        null=True,
                        verbose_name="modificado por",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="activo")),
                ("data", models.JSONField(verbose_name="data obtenida")),
                ("action", models.TextField(editable=False, verbose_name="acción")),
                (
                    "username",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
