# from rest_framework import generics, permissions
# from .models import Comment
# from .serializers import CommentSerializer

# # Xem tất cả comment
# class CommentListView(generics.ListAPIView):
#     queryset = Comment.objects.all().order_by('-created_at')
#     serializer_class = CommentSerializer

# # Tạo comment mới
# class CommentCreateView(generics.CreateAPIView):
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import connection
from .serializers import CommentSerializer
from .models import Comment

# Xem tất cả comment (dùng SQL)
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM comments_comment ORDER BY created_at DESC")
            # 'comments_comment' đổi thành đúng tên bảng của bạn (thường là <appname>_<modelname>)
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Tạo queryset giả từ danh sách id để serializer vẫn hoạt động
        ids = [r['id'] for r in rows]
        preserved = Comment.objects.filter(id__in=ids).order_by('-created_at')
        return preserved


# Tạo comment mới (dùng SQL)
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        content = request.data.get("content")

        # Thực hiện INSERT bằng SQL
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO comments_comment (user_id, content, created_at, updated_at) "
                "VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                [user_id, content]
            )

        # Trả lại dữ liệu mới tạo (lấy comment mới nhất của user)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM comments_comment WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                [user_id]
            )
            columns = [col[0] for col in cursor.description]
            row = dict(zip(columns, cursor.fetchone()))

        serializer = self.get_serializer(Comment.objects.get(pk=row["id"]))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
