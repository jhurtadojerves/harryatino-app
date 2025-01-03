# Generated by Django 3.2.13 on 2024-10-21 15:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dices", "0009_topic_permissions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topic",
            name="permissions",
            field=models.ManyToManyField(
                null=True,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Usuarios habilitados",
            ),
        ),
    ]
