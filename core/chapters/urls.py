from django.urls import path
from .views import ChapterListCreateView, get_chapter_detail

urlpatterns = [
    path('comics/<int:comic_id>/chapters/', ChapterListCreateView.as_view(), name='chapter-list-create'),
    path('<int:comic_id>/<int:chapter_id>/', get_chapter_detail, name='chapter-detail'),
]