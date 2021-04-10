"""Script to import wizards"""


def create_wizards():
    # Python
    import csv

    # Models
    from apps.profiles.models import Profile
    from django.conf import settings

    # Local
    from scripts.utils import fix_codification

    SCRIPTS_DIR = settings.BASE_DIR / "scripts"
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


def create_users():
    # Python
    import csv

    # Models
    from django.conf import settings
    from apps.authentication.models import User

    # Local
    from scripts.utils import fix_codification

    SCRIPTS_DIR = settings.BASE_DIR / "scripts"
    path = SCRIPTS_DIR / "users.csv"
    with open(path) as read_file:
        csv_reader = csv.reader(read_file, delimiter=",")
        line = 0
        # ['numero_comprador', 'id', 'nick', 'avatar',', 'nivel', 'rango_objetos', 'rango_criaturas']
        for row in csv_reader:
            try:
                pk = int(row[1])
                username = row[2]
                password = row[3]
                User.objects.create_user(pk=pk, username=username, password=password)
            except Exception as e:
                pass


create_users()
# create_wizards()
