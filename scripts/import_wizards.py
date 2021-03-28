"""Script to import wizards"""

# Python
import csv

# Models
from apps.profiles.models import Profile
from django.conf import settings

# Local
from .utils import fix_codification

SCRIPTS_DIR = settings.BASE_DIR / "scripts"


def run():
    path = SCRIPTS_DIR / "magos.csv"
    with open(path) as read_file:
        csv_reader = csv.reader(read_file, delimiter=",")
        line = 0
        # ['numero_comprador', 'id', 'nick', 'avatar',', 'nivel', 'rango_objetos', 'rango_criaturas']
        for row in csv_reader:
            try:
                data = {
                    "id": row[0],
                    "forum_user_id": row[1],
                    "nick": fix_codification(row[2]),
                    "magic_level": row[4],
                    "range_of_creatures": row[5],
                    "range_of_objects": row[6],
                    "avatar": row[3],
                }
                Profile.objects.create(**data)

            except Exception as e:
                print(e)
                print(row[0])
