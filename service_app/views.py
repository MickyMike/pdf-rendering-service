from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets, parsers
from rest_framework.decorators import api_view

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


@api_view(['GET'])
def view_document(request, pk):
    try:
        document = Document.objects.get(pk=pk)
        serializer = DocumentSerializer(document)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
