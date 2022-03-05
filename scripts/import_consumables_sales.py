"""Script to import consumables sales"""


def consumables_sales():
    # Python
    import csv
    from datetime import datetime

    # Django
    from django.conf import settings
    from django.template.loader import render_to_string

    # Models
    from apps.products.models import Product
    from apps.profiles.models import Profile
    from apps.sales.models import Sale
    from apps.authentication.models import User

    # Thirdparty integration
    import requests
    from environs import Env

    env = Env()

    API_KEY = env("API_KEY")
    SCRIPTS_DIR = settings.BASE_DIR / "scripts"
    path = SCRIPTS_DIR / "consumables_sales.csv"
    products = Product.objects.all()
    wizards = Profile.objects.all()
    sales_date = datetime(year=2022, month=3, day=5)
    user = User.objects.get(pk=1)
    # Maestra, Ilvermorny, Gryffindor, Ravenclaw, Slytherin, Hufflepuff
    keys = (
        "SCN0010021",
        "SCN0010022",
        "SCN0010017",
        "SCN0010019",
        "SCN0010020",
        "SCN0010018",
    )
    with open(path) as read_file:
        csv_reader = csv.reader(read_file, delimiter=";")
        line = 0
        for row in csv_reader:
            # User, Maestra, Ilvermorny, Gryffindor, Ravenclaw, Slytherin, Hufflepuff
            try:
                wizard = wizards.get(forum_user_id=int(row[0]))
                sales = []
                keys = {
                    "SCN0010021": row[1],
                    "SCN0010022": row[2],
                    "SCN0010017": row[3],
                    "SCN0010019": row[4],
                    "SCN0010020": row[5],
                    "SCN0010018": row[6],
                }
                for key, value in keys.items():
                    product = products.get(reference=key)
                    for num in range(0, int(value)):
                        print("oie si")
                        sales.append(
                            Sale.objects.create(
                                date=sales_date,
                                product=product,
                                profile=wizard,
                                buyer=user,
                            )
                        )
                html = render_to_string(
                    "sales/certificate.html", context={"sales": sales}
                )
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                }
                url = f"https://www.harrylatino.org/api/forums/posts?key={API_KEY}"
                topic = wizard.vault_number
                author = 121976  # Forum account for automatic post
                payload = f"topic={topic}&author={author}&post={html}"
                """response = requests.request(
                    "POST", url, headers=headers, data=payload
                )"""

            except Exception as e:
                print(e)
                print(row)


consumables_sales()
