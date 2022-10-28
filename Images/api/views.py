from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import ImageSerializer
from ..models import Image
from rest_framework.decorators import action
from wsgiref.util import FileWrapper


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @action(methods=['GET'], detail=True)
    def download(self, request, pk):
        instance = self.get_object()
        image_path = instance.clear_image.path
        image = open(image_path, 'rb')
        response = HttpResponse(FileWrapper(image), content_type='image/png')
        return response
