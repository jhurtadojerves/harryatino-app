# Generated by Django 3.2.2 on 2021-05-09 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_stockrequest_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="uploaded_image",
            field=models.ImageField(null=True, upload_to="", verbose_name="Imagen"),
        ),
    ]
