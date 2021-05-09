"""Method to get upload path"""

# Python
import os
from datetime import datetime

# Django
from config.settings.base import BASE_DIR, MEDIA_ROOT


def get_upload_path(instance, filename):
    extension = filename.split(".")[-1:]
    extension = "".join(extension)
    path = os.path.join("product", f"{instance.reference}.{extension}",)
    full_path = (
        os.path.join(BASE_DIR, MEDIA_ROOT, path)
        .replace(" ", "-")
        .replace("config/", "")
    )
    if os.path.exists(full_path):
        os.remove(full_path)
    return path
