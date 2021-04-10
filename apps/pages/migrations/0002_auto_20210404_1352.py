# Generated by Django 3.1.7 on 2021-04-04 18:52

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="content",
            field=ckeditor.fields.RichTextField(verbose_name="Contenido"),
        ),
        migrations.AlterField(
            model_name="page",
            name="name",
            field=models.CharField(
                max_length=128, unique=True, verbose_name="Nombre de la página"
            ),
        ),
        migrations.AlterField(
            model_name="page",
            name="show_in_home_page",
            field=models.BooleanField(
                default=False, verbose_name="Ver en la página de inicio"
            ),
        ),
    ]
