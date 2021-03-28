"""Get avatar to upload"""

# Python
import os

# Config
from config.settings.base import BASE_DIR, MEDIA_ROOT


def get_upload_path(instance, filename):
    extension = "".join(filename.split(".")[-1:])

    path = os.path.join(
        "authentication", "profile", "avatars", f"{instance.user.username}.{extension}",
    )
    full_path = (
        os.path.join(BASE_DIR, MEDIA_ROOT, path).replace(" ", "_").replace("conf/", "")
    )
    if os.path.exists(full_path):
        os.remove(full_path)
    return path
