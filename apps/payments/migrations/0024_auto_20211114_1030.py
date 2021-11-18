# Generated by Django 3.2.9 on 2021-11-14 15:30

import apps.payments.workflows
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0007_alter_profile_avatar"),
        ("payments", "0023_auto_20210918_1646"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                (
                    "wizard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                        verbose_name="mago",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="post",
            name="state",
            field=django_fsm.FSMIntegerField(
                choices=[
                    (0, "Cancelado"),
                    (1, "Creado"),
                    (2, "Cargado"),
                    (3, "Procesado"),
                ],
                default=apps.payments.workflows.PostWorkflow.Choices["CREATED"],
                protected=True,
                verbose_name="estado",
            ),
        ),
        migrations.CreateModel(
            name="PaymentLine",
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
                ("amount", models.FloatField(verbose_name="cantidad")),
                ("verbose", models.CharField(max_length=128, verbose_name="leyenda")),
                ("link", models.URLField(blank=True, null=True, verbose_name="url")),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payments.payment",
                        verbose_name="Pago",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
