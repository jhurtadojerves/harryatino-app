# Generated by Django 3.2.13 on 2024-10-28 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dices", "0013_alter_dice_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Road",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "message",
                    models.CharField(
                        help_text="Puedes utilizar las siguientes variables: {{result}}, {{username}}",
                        max_length=128,
                    ),
                ),
                ("result", models.IntegerField()),
                (
                    "dice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="roads",
                        to="dices.dice",
                        verbose_name="dado",
                    ),
                ),
            ],
            options={
                "ordering": ["result"],
                "unique_together": {("dice", "result")},
            },
        ),
    ]
