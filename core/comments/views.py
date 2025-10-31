from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer

# Xem tất cả comment
class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

# Tạo comment mới
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)