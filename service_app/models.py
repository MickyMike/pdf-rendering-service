from datetime import datetime

from django.db import models

from pdf_rendering_service.settings import MEDIA_URL


class Document(models.Model):
    class Status(models.TextChoices):
        PROCESSING = '1', "processing"
        DONE = '2', "done"

    file = models.FileField(max_length=60, upload_to="documents")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PROCESSING)
    pages = models.IntegerField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}"

    @property
    def filename(self):
        return f"{MEDIA_URL[1:]}{self.file}"


class Page(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    page_num = models.IntegerField()
    page_img = models.ImageField(upload_to="images")

    def __str__(self):
        return f"{self.document}_{self.page_num}"
