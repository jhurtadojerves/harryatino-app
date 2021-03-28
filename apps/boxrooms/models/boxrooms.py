"""Define models to boxroom vault"""

# Django
from django.db import models
from django.urls import reverse

# Third Party Integration Models
from ckeditor.fields import RichTextField

# Models
from tracing.models import BaseModel
from apps.profiles.models import Profile


class Boxroom(BaseModel):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.PROTECT,
        verbose_name="propietario",
        related_name="profile",
    )
    content = RichTextField()
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.slug = self.profile.forum_user_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bóveda trastero de {self.profile.nick}"

    def get_objects_creatures_or_potions_for_index(self, term):
        sales_dict = dict()
        sales_list = list()
        sales = self.profile.sales.filter(
            product__category__section__name=term
        ).order_by("date")
        if term == "Objetos":
            sales = sales.exclude(product__reference__icontains="P")
        if term == "Pociones":
            sales = self.profile.sales.filter(
                product__reference__icontains="P"
            ).order_by("date")
        for sale in sales:
            check = sales_dict.get(sale.product.reference, False)
            if not check:
                sales_dict[sale.product.reference] = {
                    "product": sale.product,
                    "sales": 1,
                    "date": sale.date,
                }
            else:
                sales = check.get("sales") + 1
                date = check.get("date")
                sales_dict.update(
                    {
                        sale.product.reference: {
                            "product": sale.product,
                            "sales": sales,
                            "date": date,
                        }
                    }
                )

        for sale in sales_dict.values():
            sales_list.append(sale)
        sales_list.sort(key=lambda x: x.get("date"))
        return sales_list

    def detail_objects_creatures_or_potions(self, term):
        return self.profile.sales.filter(
            product__category__section__name=term
        ).order_by("date")

    def get_objects_list(self):
        return self.detail_objects_creatures_or_potions("Objetos").exclude(
            product__reference__icontains="P"
        )

    def get_potions_list(self):
        return self.profile.sales.filter(product__reference__icontains="P").order_by(
            "date"
        )

    def get_objects_index(self):
        return self.get_objects_creatures_or_potions_for_index("Objetos")

    def get_creatures_index(self):
        return self.get_objects_creatures_or_potions_for_index("Criaturas")

    def get_potions_index(self):
        return self.get_objects_creatures_or_potions_for_index("Pociones")

    def get_books_index(self):
        return self.profile.sales.filter(product__category__name="LH").order_by("date")

    def get_consumables_list(self):
        return self.profile.sales.filter(product__category__name="CS").order_by("date")

    def get_absolute_url(self):
        return reverse("boxroom:boxroom_detail", args=[str(self.slug)])

    def update_url(self):
        return reverse("boxroom:boxroom_update", args=[str(self.slug)])

    def detail_url(self):
        return self.get_absolute_url()

    class Meta(BaseModel.Meta):
        verbose_name = "bóveda trastero"
        verbose_name_plural = "bóvedas trastero"
