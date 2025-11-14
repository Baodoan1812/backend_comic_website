# from rest_framework import generics, permissions
# from .models import Comic
# from .serializers import ComicSerializer
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# class ComicCreateView(generics.CreateAPIView):
#     queryset = Comic.objects.all()
#     serializer_class = ComicSerializer
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)

# class ComicListView(generics.ListAPIView):
#     queryset = Comic.objects.all().order_by('-id')
#     serializer_class = ComicSerializer

# class ComicUpdateView(generics.UpdateAPIView):
#     queryset = Comic.objects.all()
#     lookup_field = 'id'
#     serializer_class = ComicSerializer

# class ComicDetailView(generics.RetrieveAPIView):
#     queryset = Comic.objects.all()
#     serializer_class = ComicSerializer
#     lookup_field = 'id'

# @api_view(['GET'])
# def top_comics(request):
#     comics = Comic.objects.all().order_by('-read_count')[:3]
#     serializer = ComicSerializer(comics, many=True, context={'request': request})
#     return Response(serializer.data)

# @api_view(['GET'])
# def latest_comics(request):
#     comics = Comic.objects.all().order_by('-updated_at')[:8]
#     serializer = ComicSerializer(comics, many=True, context={'request': request})
#     return Response(serializer.data)

from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from .models import Comic
from .serializers import ComicSerializer

TABLE_NAME = "comics_comic"


# --------------------- TẠO COMIC (INSERT) ---------------------

class ComicCreateView(generics.CreateAPIView):
    serializer_class = ComicSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user.id
        author = data.get('author', '')
        genre= data.get('genre', '')
        title = data.get('title')
        description = data.get('description', '')
        read_count = 0
        cover_image = data.get('cover_image')  # file

        # Upload ảnh bằng Django, còn lại dùng raw SQL
        comic = Comic.objects.create(
            title=title,
            description=description,
            author=author,
            genre=genre,
            created_by_id=user,
            cover_image=cover_image
        )

        # Dùng raw SQL cập nhật read_count = 0 (ví dụ)
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE comics_comic SET read_count = %s WHERE id = %s",
                [read_count, comic.id]
            )

        serializer = ComicSerializer(comic, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------- DANH SÁCH COMIC (SELECT) ---------------------
class ComicListView(generics.ListAPIView):
    serializer_class = ComicSerializer

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM {TABLE_NAME} ORDER BY id DESC")
            ids = [row[0] for row in cursor.fetchall()]
        return Comic.objects.filter(id__in=ids).order_by("-id")


# --------------------- CẬP NHẬT COMIC (UPDATE) ---------------------
class ComicUpdateView(generics.UpdateAPIView):
    serializer_class = ComicSerializer
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        comic_id = kwargs.get("id")
        data = request.data

        if not data:
            return Response({"error": "No data provided"}, status=400)

        # Tạo danh sách cột và giá trị cần update
        set_clauses = []
        values = []
        for field in ["title", "author", "genre", "description", "read_count"]:
            if field in data:
                set_clauses.append(f"{field}=%s")
                values.append(data[field])

        if not set_clauses:
            return Response({"error": "No valid fields to update"}, status=400)

        # Thêm updated_at
        set_clauses.append("updated_at=CURRENT_TIMESTAMP")
        sql_set = ", ".join(set_clauses)

        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {TABLE_NAME} SET {sql_set} WHERE id=%s",
                values + [comic_id]
            )

        comic = Comic.objects.get(pk=comic_id)
        serializer = self.get_serializer(comic)
        return Response(serializer.data)




# --------------------- CHI TIẾT COMIC (SELECT ONE) ---------------------
class ComicDetailView(generics.RetrieveAPIView):
    serializer_class = ComicSerializer
    lookup_field = "id"

    def get_object(self):
        comic_id = self.kwargs.get("id")
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM {TABLE_NAME} WHERE id = %s", [comic_id])
            row = cursor.fetchone()
        if not row:
            from rest_framework.exceptions import NotFound
            raise NotFound("Comic not found")
        return Comic.objects.get(pk=row[0])


# --------------------- TOP 3 COMIC (ORDER BY read_count) ---------------------
@api_view(["GET"])
def top_comics(request):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id FROM {TABLE_NAME} ORDER BY read_count DESC LIMIT 3")
        ids = [row[0] for row in cursor.fetchall()]
    comics = Comic.objects.filter(id__in=ids).order_by("-read_count")
    serializer = ComicSerializer(comics, many=True, context={"request": request})
    return Response(serializer.data)


# --------------------- LATEST COMIC (ORDER BY updated_at) ---------------------
@api_view(["GET"])
def latest_comics(request):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id FROM {TABLE_NAME} ORDER BY updated_at DESC LIMIT 8")
        ids = [row[0] for row in cursor.fetchall()]
    comics = Comic.objects.filter(id__in=ids).order_by("-updated_at")
    serializer = ComicSerializer(comics, many=True, context={"request": request})
    return Response(serializer.data)
