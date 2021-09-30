from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.conf import settings

from .constants import PDF_FOLDER, IMG_FOLDER


class Document(models.Model):
    class Status(models.TextChoices):
        PROCESSING = "processing", "1"
        DONE = "done", "2"

    pdf_file = models.FileField(
        max_length=60,
        upload_to=PDF_FOLDER,
        validators=[FileExtensionValidator(["pdf"])],
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PROCESSING
    )
    pages = models.IntegerField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}"

    @property
    def filename(self):
        return f"{settings.MEDIA_URL[1:]}{self.pdf_file}"


class Page(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    page_num = models.IntegerField()
    page_img = models.ImageField(upload_to=IMG_FOLDER)

    def __str__(self):
        return f"{self.document}_{self.page_num}"


# solution for autodeleting files on removal from db, which was used during development
# https://cmljnelson.blog/2020/06/22/delete-files-when-deleting-models-in-django/
