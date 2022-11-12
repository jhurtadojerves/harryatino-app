# Python
import os

# Django
from config.settings.base import BASE_DIR, MEDIA_ROOT


def get_upload_path(instance, filename):
    extension = filename.split(".")[-1:]
    extension = "".join(extension)
    path = os.path.join(
        "profile",
        f"{instance.forum_user_id}.{extension}",
    )
    full_path = (
        os.path.join(BASE_DIR, MEDIA_ROOT, path)
        .replace(" ", "-")
        .replace("config/", "")
    )

    if os.path.exists(full_path):
        os.remove(full_path)

    return path
