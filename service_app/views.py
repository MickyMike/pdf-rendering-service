from django.http.response import JsonResponse
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets, parsers

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewset(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']


class DocumentUploadView(generics.GenericAPIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.FileUploadParser]
    serializer_class = DocumentSerializer

    def post(self, request):
        up_file = request.FILES['file']
        print(up_file.name)

        return JsonResponse({"koko": up_file.name}, status=status.HTTP_201_CREATED)
