# Generated by Django 3.2 on 2021-04-25 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0003_auto_20210424_2222"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="field",
            name="container",
        ),
        migrations.DeleteModel(
            name="Choice",
        ),
        migrations.DeleteModel(
            name="Container",
        ),
        migrations.DeleteModel(
            name="Field",
        ),
    ]
