# Generated by Django 3.2.7 on 2021-09-26 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(max_length=60, upload_to=''),
        ),
    ]
