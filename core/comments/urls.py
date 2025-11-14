from django.urls import path
from .views import CommentListView, CommentCreateView, CommentByComicView

urlpatterns = [
    path('', CommentListView.as_view(), name='comment-list'),
    path('create/', CommentCreateView.as_view(), name='comment-create'),
     path("comic/<int:comic_id>/", CommentByComicView.as_view(), name="comment-by-comic"),
]