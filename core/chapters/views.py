# from rest_framework import generics, permissions
# from .models import Chapter
# from .serializers import ChapterSerializer
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# # Lấy danh sách chapter theo comic ID và tạo chapter mới
# class ChapterListCreateView(generics.ListCreateAPIView):
#     serializer_class = ChapterSerializer
#     permission_classes = [permissions.AllowAny]  # có thể đổi sang IsAuthenticated

#     def get_queryset(self):
#         comic_id = self.kwargs['comic_id']
#         return Chapter.objects.filter(comic_id=comic_id).order_by('number')

#     def perform_create(self, serializer):
#         comic_id = self.kwargs['comic_id']
#         serializer.save(
#             comic_id=comic_id,
#             created_by=self.request.user if self.request.user.is_authenticated else None
#         )

# @api_view(['GET'])
# def get_chapter_detail(request, comic_id, chapter_id):
#     try:
#         chapter = Chapter.objects.get(comic__id=comic_id, id=chapter_id)
#     except Chapter.DoesNotExist:
#         return Response({'error': 'Chapter not found'}, status=404)

#     serializer = ChapterSerializer(chapter, context={'request': request})
#     return Response(serializer.data)
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import connection
from django.core.files.storage import default_storage
from django.conf import settings
from urllib.parse import urljoin
from .serializers import ChapterSerializer
from .models import Chapter


class ChapterListCreateView(generics.GenericAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, comic_id):
        """
        Lấy danh sách chapter theo comic_id (dùng raw SQL)
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, number, title, content, image, comic_id, created_by_id, created_at, updated_at
                FROM chapters_chapter
                WHERE comic_id = %s
                ORDER BY number ASC
            """, [comic_id])
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Chuyển đường dẫn ảnh thành URL tuyệt đối (http://localhost:8000/media/...)
        for r in results:
            if r.get("image"):
                if not r["image"].startswith(settings.MEDIA_URL):
                    r["image"] = urljoin(settings.MEDIA_URL, r["image"])
                r["image"] = request.build_absolute_uri(r["image"])

        return Response(results, status=status.HTTP_200_OK)

    def post(self, request, comic_id):
        """
        Tạo chapter mới (dùng raw SQL + upload ảnh)
        """
        data = request.data
        number = data.get("number")
        title = data.get("title")
        content = data.get("content")
        image_file = request.FILES.get("image")
        created_by_id = request.user.id if request.user.is_authenticated else None

        # Lưu ảnh (nếu có)
        image_path = None
        if image_file:
            image_path = default_storage.save(f"chapters/{image_file.name}", image_file)

        # Thêm dữ liệu vào DB
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO chapters_chapter (number, title, content, image, comic_id, created_by_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                RETURNING id, number, title, content, image, comic_id, created_by_id, created_at, updated_at
            """, [number, title, content, image_path, comic_id, created_by_id])
            columns = [col[0] for col in cursor.description]
            chapter = dict(zip(columns, cursor.fetchone()))

        # Trả URL ảnh đầy đủ
        if chapter.get("image"):
            if not chapter["image"].startswith(settings.MEDIA_URL):
                chapter["image"] = urljoin(settings.MEDIA_URL, chapter["image"])
            chapter["image"] = request.build_absolute_uri(chapter["image"])

        return Response(chapter, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_chapter_detail(request, comic_id, chapter_id):
    """
    Lấy chi tiết 1 chapter (dùng raw SQL)
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, number, title, content, image, comic_id, created_by_id, created_at, updated_at
            FROM chapters_chapter
            WHERE comic_id = %s AND id = %s
            LIMIT 1
        """, [comic_id, chapter_id])
        row = cursor.fetchone()

        if not row:
            return Response({"error": "Chapter not found"}, status=status.HTTP_404_NOT_FOUND)

        columns = [col[0] for col in cursor.description]
        chapter = dict(zip(columns, row))

    # Chuyển ảnh thành URL đầy đủ
    if chapter.get("image"):
        if not chapter["image"].startswith(settings.MEDIA_URL):
            chapter["image"] = urljoin(settings.MEDIA_URL, chapter["image"])
        chapter["image"] = request.build_absolute_uri(chapter["image"])

    return Response(chapter, status=status.HTTP_200_OK)
