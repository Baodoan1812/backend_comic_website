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
from comics.models import Comic

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

class CommentByComicView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        comic_id = self.kwargs.get("comic_id")  # lấy từ URL param
        if not comic_id:
            return Comment.objects.none()  # trả về rỗng nếu không có comic_id

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM comments_comment WHERE comic_id = %s ORDER BY created_at DESC",
                [comic_id]
            )
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
        comic_id = request.data.get("comic_id")  # có thể None

        # validate content bắt buộc, comic_id optional
        if not content:
            return Response({"error": "content is required"}, status=400)

        comic = None
        if comic_id:  # nếu có comic_id mới kiểm tra tồn tại
            try:
                comic = Comic.objects.get(id=comic_id)
            except Comic.DoesNotExist:
                return Response({"error": "Comic not found"}, status=404)

        # INSERT
        with connection.cursor() as cursor:
            if comic_id:  # có comic_id
                cursor.execute(
                    "INSERT INTO comments_comment (user_id, comic_id, content, created_at, updated_at) "
                    "VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                    [user_id, comic_id, content]
                )
            else:  # không có comic_id
                cursor.execute(
                    "INSERT INTO comments_comment (user_id, content, created_at, updated_at) "
                    "VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                    [user_id, content]
                )

        # SELECT comment vừa tạo (lấy comment mới nhất của user)
        with connection.cursor() as cursor:
            if comic_id:
                cursor.execute(
                    "SELECT * FROM comments_comment WHERE user_id = %s AND comic_id = %s ORDER BY id DESC LIMIT 1",
                    [user_id, comic_id]
                )
            else:
                cursor.execute(
                    "SELECT * FROM comments_comment WHERE user_id = %s AND comic_id IS NULL ORDER BY id DESC LIMIT 1",
                    [user_id]
                )
            row_data = cursor.fetchone()
            if not row_data:
                return Response({"error": "Failed to create comment"}, status=500)
            columns = [col[0] for col in cursor.description]
            row = dict(zip(columns, row_data))

        serializer = self.get_serializer(Comment.objects.get(pk=row["id"]))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
