"""Script to import products"""


def products():
    # Python
    import csv

    # Django
    from django.conf import settings

    # Models
    from apps.products.models import Product, Section, Category

    # Local
    from scripts.utils import fix_codification

    SCRIPTS_DIR = settings.BASE_DIR / "scripts"
    path = SCRIPTS_DIR / "Products.csv"
    print(path)
    with open(path) as read_file:
        csv_reader = csv.reader(read_file, delimiter=";")
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


def create_sections():
    # Python
    import csv

    # Django
    from django.conf import settings

    # Models
    from apps.products.models import Product, Section, Category

    # Local
    from scripts.utils import fix_codification

    SCRIPTS_DIR = settings.BASE_DIR / "scripts"
    path = SCRIPTS_DIR / "products_section.csv"
    with open(path) as read_file:
        csv_reader = csv.reader(read_file, delimiter=",")
        for row in csv_reader:
            try:
                pk = int(row[3])
                name = row[0]
                order = int(row[1])
                slug = row[2]
                Section.objects.update_or_create(
                    pk=pk, name=name, slug=slug, defaults={"order": order}
                )
            except Exception as e:
                print(e)


def create_categories():
    # Python
    import csv

    # Django
    from django.conf import settings

    # Models
    from apps.products.models import Product, Section, Category

    # Local
    from scripts.utils import fix_codification

    SCRIPTS_DIR = settings.BASE_DIR / "scripts"
    path = SCRIPTS_DIR / "products_category.csv"
    with open(path) as read_file:
        csv_reader = csv.reader(read_file, delimiter=",")
        for row in csv_reader:
            try:
                pk = row[0]
                name = row[1]
                section_id = row[2]
                Category.objects.update_or_create(
                    pk=pk, defaults={"section_id": section_id, "name": name}
                )
            except Exception as e:
                print(e)


create_sections()
create_categories()
products()
