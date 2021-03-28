"""Script to import sales"""

# Python
import csv
from datetime import datetime

# Models
from apps.sales.models import Sale
from apps.profiles.models import Profile
from apps.products.models import Product
from apps.authentication.models import User

# Django
from django.conf import settings
from django.db.models.signals import post_save

SCRIPTS_DIR = settings.BASE_DIR / "scripts"


def run():
    path = SCRIPTS_DIR / "transacciones.csv"
    with open(path) as read_file:
        csv_reader = csv.reader(read_file, delimiter=",")
        line = 0
        # ['numero', 'fecha', 'referencia', 'forum_id',', 'vendedor']
        for row in csv_reader:
            try:
                raw_date = row[1].split("-")
                date = datetime(int(raw_date[0]), int(raw_date[1]), int(raw_date[2]))
                product = Product.objects.get(reference=row[2])
                profile = Profile.objects.get(forum_user_id=row[3])
                # user = User.objects.get(old_number=row[4])
                user = User.objects.get(pk=1)
                data = {
                    "date": date,
                    "product": product,
                    "profile": profile,
                    "created_user": user,
                }
                Sale.objects.create(**data)
            except Exception as e:
                print(e)
