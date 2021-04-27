# Generated by Django 3.1.7 on 2021-03-14 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                    "forum_user_id",
                    models.PositiveIntegerField(
                        unique=True, verbose_name="Id del foro"
                    ),
                ),
                ("nick", models.CharField(max_length=128)),
                (
                    "magic_level",
                    models.PositiveIntegerField(verbose_name="Nivel Mágico"),
                ),
                (
                    "range_of_creatures",
                    models.CharField(max_length=8, verbose_name="Rango de Criaturas"),
                ),
                (
                    "range_of_objects",
                    models.CharField(max_length=8, verbose_name="Rango de Objetos"),
                ),
                (
                    "vault",
                    models.URLField(blank=True, null=True, verbose_name="Bóveda"),
                ),
                ("avatar", models.URLField()),
            ],
            options={
                "verbose_name": "Mago",
                "verbose_name_plural": "Magos",
                "ordering": ("pk",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SocialRank",
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
                    "name",
                    models.CharField(
                        max_length=128, unique=True, verbose_name="Nombre"
                    ),
                ),
                (
                    "initial_points",
                    models.PositiveIntegerField(verbose_name="Puntos de Desde"),
                ),
                (
                    "end_points",
                    models.PositiveIntegerField(verbose_name="Puntos de Hasta"),
                ),
                ("slug", models.SlugField(editable=False, max_length=256)),
            ],
            options={
                "verbose_name": "Rango Social",
                "verbose_name_plural": "Rangos Sociales",
                "abstract": False,
            },
        ),
    ]