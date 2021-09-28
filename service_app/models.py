from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator

from pdf_rendering_service.settings import MEDIA_URL


class Document(models.Model):
    class Status(models.TextChoices):
        PROCESSING = "processing", '1'
        DONE = "done", '2'

    pdf_file = models.FileField(max_length=60, upload_to="documents", validators=[FileExtensionValidator(["pdf"])])
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PROCESSING)
    pages = models.IntegerField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}"

    @property
    def filename(self):
        return f"{MEDIA_URL[1:]}{self.pdf_file}"


class Page(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    page_num = models.IntegerField()
    page_img = models.ImageField(upload_to="images")

    def __str__(self):
        return f"{self.document}_{self.page_num}"


# solution for autodeleting files on removal from db
# https://cmljnelson.blog/2020/06/22/delete-files-when-deleting-models-in-django/

""" Whenever ANY model is deleted, if it has a file field on it, delete the associated file too"""
@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance, field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)


""" Delete the file if something else get uploaded in its place"""
@receiver(pre_save)
def delete_files_when_file_changed(sender, instance, **kwargs):
    # Don't run on initial save
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            # its got a file field. Let's see if it changed
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                # We are probably in a transaction and the PK is just temporary
                # Don't worry about deleting attachments if they aren't actually saved yet.
                return
            instance_in_db_file_field = getattr(instance_in_db, field.name)
            instance_file_field = getattr(instance, field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender, instance, field, instance_in_db_file_field)


""" Only delete the file if no other instances of that model are using it"""
def delete_file_if_unused(model, instance, field, instance_file_field):
    dynamic_field = {field.name: instance_file_field.name}
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)
