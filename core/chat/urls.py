from django.urls import path
from .views import ChatListView, ChatCreateView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-list'),       # Lấy danh sách chat
    path('create/', ChatCreateView.as_view(), name='chat-create'),  # Tạo chat mới
]