# Generated by Django 3.2.5 on 2021-07-11 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0009_school_schoolpayment_schoolpaymentline"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="school",
            options={"verbose_name": "Escuela Mágica"},
        ),
        migrations.AlterModelOptions(
            name="schoolpayment",
            options={"verbose_name": "Pago Escuela"},
        ),
    ]