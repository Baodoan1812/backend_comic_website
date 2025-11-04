from django.urls import path
from .views import ComicCreateView, ComicListView, ComicUpdateView, ComicDetailView, top_comics, latest_comics

urlpatterns = [
    path('create/', ComicCreateView.as_view(), name='comic-create'),
    path('', ComicListView.as_view(), name='comic-list'),
    path('<int:id>/update/', ComicUpdateView.as_view(), name='comic-update'),
    path('<int:id>/', ComicDetailView.as_view(), name='comic-detail'),
    path('top/', top_comics, name='comic-top'),
    path('latest/', latest_comics, name='comic-latest'),
]
