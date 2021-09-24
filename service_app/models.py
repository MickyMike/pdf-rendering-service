from django.db import models


class Document(models.Model):
    document_id = models.BigAutoField(primary_key=True)
    pages_num = models.IntegerField()


class Page(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    page_num = models.IntegerField()
    page_img = models.BinaryField()
