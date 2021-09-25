from rest_framework import serializers
from .models import Document, Page


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['pk', 'document_id', 'page_num', 'page_img']