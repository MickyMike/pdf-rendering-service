import dramatiq
from pdf2image import convert_from_bytes

from .models import Document, Page


@dramatiq.actor
def render_images(pk):
    document = Document.objects.get(pk=pk)

    try:
        with open(document.filename, "rb") as f:
            images = convert_from_bytes(f.read(), size=(1200, 1600))
        document.status = Document.Status.DONE
        document.save()
        for i in range(len(images)):
            images[i].save('page' + str(i) + '.png', 'PNG')
    except Exception as e:
        print(e)
