# Generated by Django 4.0.3 on 2022-03-14 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sales", "0005_sale_is_award"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sale",
            options={
                "ordering": ("id",),
                "verbose_name": "Venta",
                "verbose_name_plural": "Ventas",
            },
        ),
        migrations.AddField(
            model_name="sale",
            name="consumable_comment",
            field=models.TextField(blank=True, null=True, verbose_name="Comentario"),
        ),
        migrations.AddField(
            model_name="sale",
            name="consumable_url",
            field=models.URLField(null=True, verbose_name="URL uso"),
        ),
        migrations.AlterField(
            model_name="sale",
            name="available",
            field=models.BooleanField(
                default=True,
                help_text="Este campo se utiliza para marcar una compra de libros de hechizos o consumibles. <br>Libros de Hechizos. Marcado = Se puede usar<br>Consumibles. Desmarcado = Consumible utilizado<br>Criaturas (Premios y/o Régimen Transitorio). Desmarcado = La criatura se encuentra en la reserva de animales<br>",
                verbose_name="Disponible?",
            ),
        ),
    ]
