from django.urls import path
from .views import ComicCreateView, ComicListView, ComicUpdateView, ComicDetailView

urlpatterns = [
    path('create/', ComicCreateView.as_view(), name='comic-create'),
    path('', ComicListView.as_view(), name='comic-list'),
    path('<int:id>/update/', ComicUpdateView.as_view(), name='comic-update'),
    path('<int:id>/', ComicDetailView.as_view(), name='comic-detail'),
]
