# Generated by Django 3.2.3 on 2021-05-18 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dynamicforms", "0004_alter_action_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="form",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="dynamicforms.form",
                verbose_name="formulario",
            ),
        ),
    ]
