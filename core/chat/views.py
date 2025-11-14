from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import connection
from .serializers import ChatSerializer
from .models import Chat

# Lấy tất cả chat
class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM chat_chat ORDER BY created_at DESC")
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        ids = [r['id'] for r in rows]
        preserved = Chat.objects.filter(id__in=ids).order_by('-created_at')
        return preserved

# Tạo chat mới
class ChatCreateView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        content = request.data.get("content")

        if not content:
            return Response({"error": "content is required"}, status=400)

        # INSERT
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO chat_chat (user_id, content, created_at, updated_at) "
                "VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                [user_id, content]
            )

        # SELECT chat vừa tạo
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM chat_chat WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                [user_id]
            )
            row_data = cursor.fetchone()
            if not row_data:
                return Response({"error": "Failed to create chat"}, status=500)
            columns = [col[0] for col in cursor.description]
            row = dict(zip(columns, row_data))

        serializer = self.get_serializer(Chat.objects.get(pk=row["id"]))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
