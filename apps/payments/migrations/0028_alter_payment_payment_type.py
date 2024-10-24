# Generated by Django 4.0.3 on 2022-03-19 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0027_remove_paymentline_short_link_payment_html_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="payment_type",
            field=models.SmallIntegerField(
                choices=[(0, "Compra"), (1, "Pluses"), (99, "Otro")],
                default=0,
                verbose_name="Tipo de pago",
            ),
        ),
    ]
