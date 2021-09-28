import os

import dramatiq
from pdf2image import convert_from_bytes

from .models import Document, Page
from .constants import IMG_FOLDER
from pdf_rendering_service.settings import MEDIA_URL


@dramatiq.actor
def render_images(pk):
    document = Document.objects.get(pk=pk)
    os.makedirs(IMG_FOLDER, exist_ok=True)

    try:
        with open(document.filename, "rb") as f:
            images = convert_from_bytes(f.read(), size=(1200, 1600))
        for i, image in enumerate(images):
            path = f"{IMG_FOLDER}/{pk}_{str(i+1)}.png"
            image.save(f"{MEDIA_URL[1:]}{path}", 'PNG')
            page = Page(document=document, page_num=i+1, page_img=path)
            page.save()

        document.status = Document.Status.DONE
        document.pages = len(images)
        document.save()
    except Exception as e:
        print(e)
