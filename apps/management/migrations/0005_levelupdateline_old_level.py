# Generated by Django 3.2.13 on 2025-02-06 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0004_alter_levelupdate_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="levelupdateline",
            name="old_level",
            field=models.IntegerField(default=0),
        ),
    ]
