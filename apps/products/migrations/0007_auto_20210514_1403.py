# Generated by Django 3.2.3 on 2021-05-14 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_section_available_by_default"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="section",
            name="available_by_default",
        ),
        migrations.AddField(
            model_name="category",
            name="available_by_default",
            field=models.BooleanField(default=True),
        ),
    ]
