from rest_framework import generics, permissions
from .models import Comic
from .serializers import ComicSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class ComicCreateView(generics.CreateAPIView):
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ComicListView(generics.ListAPIView):
    queryset = Comic.objects.all().order_by('-id')  # sắp xếp mới nhất trước
    serializer_class = ComicSerializer

class ComicUpdateView(generics.UpdateAPIView):
    queryset = Comic.objects.all()
    lookup_field = 'id'
    serializer_class = ComicSerializer

class ComicDetailView(generics.RetrieveAPIView):
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    lookup_field = 'id'