# Generated by Django 3.2.13 on 2022-11-06 19:25

import config.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dices", "0002_auto_20221104_1004"),
    ]

    operations = [
        migrations.AddField(
            model_name="roll",
            name="post_url",
            field=config.fields.CustomURLField(
                null=True, verbose_name="Posteo en el foro"
            ),
        ),
    ]