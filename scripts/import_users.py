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
            pk = int(row[1])
            username = row[2]
            password = row[3]
            try:
                User.objects.create_user(pk=pk, username=username, password=password)
            except Exception as e:
                user = User.objects.get(pk=pk)
                user.old_number = int(row[0])
                user.save()


create_users()
