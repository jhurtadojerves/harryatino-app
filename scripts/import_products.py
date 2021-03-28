"""Script to import products"""

# Python
import csv

# Django
from django.conf import settings

# Models
from apps.products.models import Product, Section, Category

# Local
from .utils import fix_codification


SCRIPTS_DIR = settings.BASE_DIR / "scripts"


def run():
    path = SCRIPTS_DIR / "productos.csv"
    with open(path) as read_file:
        csv_reader = csv.reader(read_file, delimiter=",")
        line = 0
        for row in csv_reader:
            try:
                section = Section.objects.get(name=row[2])
                category = Category.objects.get(name=row[4])
                data = {
                    "name": fix_codification(row[3]),
                    "reference": row[1],
                    "points": row[5],
                    "cost": row[6],
                    "initial_stock": row[7],
                    "image": row[8],
                    "description": fix_codification(row[9]),
                    "category": category,
                }
                product = Product.objects.create(**data)
                product.slug = product.reference
                product.save()
            except Exception as e:
                print(e)
