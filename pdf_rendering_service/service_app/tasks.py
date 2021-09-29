import os
import logging

from PIL import Image
import dramatiq
from pdf2image import convert_from_bytes
from pdf2image.exceptions import PDFPageCountError
from django.conf import settings

from .models import Document, Page
from .constants import IMG_FOLDER


def render(filename: str) -> list[Image]:
    try:
        with open(filename, "rb") as f:
            images = convert_from_bytes(f.read(), size=(1200, 1600))
            return images
    except FileNotFoundError as e:
        logging.error(e)
    except PDFPageCountError as e:
        logging.error(e)
    return []


@dramatiq.actor
def render_images(pk):
    document = Document.objects.get(pk=pk)
    os.makedirs(f"{settings.MEDIA_URL[1:]}{IMG_FOLDER}", exist_ok=True)

    images = render(document.filename)

    for i, image in enumerate(images):
        path = f"{IMG_FOLDER}/{pk}_{str(i+1)}.png"
        image.save(f"{settings.MEDIA_URL[1:]}{path}", "PNG")
        page = Page(document=document, page_num=i + 1, page_img=path)
        page.save()

    document.status = Document.Status.DONE
    document.pages = len(images)
    document.save()
