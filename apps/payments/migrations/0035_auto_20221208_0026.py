# Generated by Django 3.2.13 on 2022-12-08 05:26

import apps.payments.workflows
from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0034_monthpaymentline_state"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="monthpaymentline",
            options={"ordering": ("state", "work__wizard__nick")},
        ),
        migrations.AlterField(
            model_name="monthpayment",
            name="state",
            field=django_fsm.FSMIntegerField(
                choices=[
                    (0, "Cancelado"),
                    (1, "Creado"),
                    (2, "Calculado"),
                    (3, "Pagado"),
                    (4, "Sin pago"),
                ],
                default=apps.payments.workflows.MonthlyPaymentWorkflow.Choices[
                    "CREATED"
                ],
                protected=True,
                verbose_name="estado",
            ),
        ),
        migrations.AlterField(
            model_name="monthpaymentline",
            name="state",
            field=django_fsm.FSMIntegerField(
                choices=[
                    (0, "Cancelado"),
                    (1, "Creado"),
                    (2, "Calculado"),
                    (3, "Pagado"),
                    (4, "Sin pago"),
                ],
                default=apps.payments.workflows.MonthlyPaymentWorkflow.Choices[
                    "CREATED"
                ],
                protected=True,
                verbose_name="estado",
            ),
        ),
    ]