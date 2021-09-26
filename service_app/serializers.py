from rest_framework import serializers
from .models import Document, Page


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file']
        read_only_fields = ["status"]


class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['document', 'page_num', 'page_img']
