from rest_framework import serializers
from .models import Document, Page


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ['document_id', 'pages_num', 'inserted']


class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['pk', 'document_id', 'page_num', 'page_img']