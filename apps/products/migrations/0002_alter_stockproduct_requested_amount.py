# Generated by Django 3.2 on 2021-04-08 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stockproduct",
            name="requested_amount",
            field=models.PositiveIntegerField(verbose_name="Cantidad a Aumentar"),
        ),
    ]
