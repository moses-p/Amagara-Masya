from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Photo, Child
from .serializers import PhotoSerializer, ChildSerializer

class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticated]

class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        child_id = self.kwargs.get('child_pk')
        if child_id:
            return Photo.objects.filter(child_id=child_id)
        return Photo.objects.none()

    def perform_create(self, serializer):
        child_id = self.kwargs.get('child_pk')
        serializer.save(child_id=child_id)

class ChildPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Photo.objects.filter(child_id=self.kwargs['child_pk'])

    def perform_create(self, serializer):
        serializer.save(child_id=self.kwargs['child_pk']) 