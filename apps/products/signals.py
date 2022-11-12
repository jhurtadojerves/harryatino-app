from io import BytesIO

import requests

# Django
from django.core import files


def download_from_imgur_and_upload(sender, instance, created, **kwargs):
    if not instance.uploaded_image and instance.image:
        response = requests.get(instance.image, stream=True)

        if response.status_code == requests.codes.ok:
            file_name = instance.image.split("/")[-1]
            fp = BytesIO()
            fp.write(response.content)
            instance.uploaded_image.save(file_name, files.File(fp))
