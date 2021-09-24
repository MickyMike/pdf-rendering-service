from datetime import datetime

from django.db import models


class Document(models.Model):
    def __str__(self):
        return f"{self.document_id}"

    document_id = models.BigAutoField(primary_key=True)
    pages_num = models.IntegerField()
    inserted = models.DateTimeField(default=datetime.now, blank=True)


class Page(models.Model):
    def __str__(self):
        return f"{self.document_id}_{self.page_num}"

    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    page_num = models.IntegerField()
    page_img = models.BinaryField()
