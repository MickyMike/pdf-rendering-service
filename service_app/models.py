from datetime import datetime

from django.db import models

from pdf_rendering_service.settings import MEDIA_URL


class Document(models.Model):
    class Status(models.TextChoices):
        PROCESSING = '1', "processing"
        DONE = '2', "done"

    file = models.FileField(max_length=60)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PROCESSING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def filename(self):
        return f"{MEDIA_URL}{self.file}"


class Page(models.Model):
    def __str__(self):
        return f"{self.document_id}_{self.page_num}"

    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    page_num = models.IntegerField()
    page_img = models.BinaryField()
