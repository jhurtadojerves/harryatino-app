# Generated by Django 3.2.13 on 2024-10-20 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dices", "0006_topic_state"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="topic",
            options={
                "permissions": (("can_manage", "Can manage dices"),),
                "verbose_name": "topic",
                "verbose_name_plural": "topics para dados",
            },
        ),
    ]
