from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets, parsers
from rest_framework.decorators import api_view

from .models import Document
from .serializers import DocumentSerializer
from .tasks import render_images


class DocumentUploadView(generics.GenericAPIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    serializer_class = DocumentSerializer

    def post(self, request, *args, **kwargs):
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
            serializer = DocumentSerializer(document)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_document(request, pk):
    try:
        document = Document.objects.get(pk=pk)
        serializer = DocumentSerializer(document)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
