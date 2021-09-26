from django.http.response import JsonResponse, FileResponse
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import parsers

from .models import Document, Page
from .serializers import DocumentSerializer, PageSerializer
from .tasks import render_images


class DocumentUploadView(generics.GenericAPIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    serializer_class = DocumentSerializer

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            document = serializer.save()
            render_images.send(document.pk)
            return JsonResponse({"id": document.pk}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentView(generics.GenericAPIView):

    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
            return JsonResponse({"status": document.status, "n_pages": document.pages}, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            raise Http404("Document does not exist")


class PageView(generics.GenericAPIView):

    def get(self, request, pk, num):
        try:
            page = Page.objects.get(page_num=num, document=pk).page_img
            serializer = PageSerializer(page)
            return FileResponse(page, content_type='image/png')
        except Page.DoesNotExist:
            raise Http404("Page does not exist")
