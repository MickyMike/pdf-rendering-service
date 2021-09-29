from django.http.response import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework import parsers

from .models import Document, Page
from .serializers import DocumentSerializer
from .tasks import render_images


class DocumentUploadView(generics.GenericAPIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    serializer_class = DocumentSerializer

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        render_images.send(document.pk)
        return JsonResponse({"id": document.pk}, status=status.HTTP_201_CREATED)


class DocumentView(generics.GenericAPIView):

    def get(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        return JsonResponse({"status": document.status, "n_pages": document.pages}, status=status.HTTP_200_OK)


class PageView(generics.GenericAPIView):

    def get(self, request, pk, num):
        page_img = get_object_or_404(Page, page_num=num, document=pk).page_img
        return FileResponse(page_img, content_type='image/png')
