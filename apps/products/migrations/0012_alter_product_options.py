# Generated by Django 4.1 on 2022-09-01 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0011_product_can_be_sold"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ("-can_be_sold", "category__name", "name"),
                "verbose_name": "Producto",
                "verbose_name_plural": "Productos",
            },
        ),
    ]
