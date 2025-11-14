from django.contrib import admin
from .models import Comment   # import model

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comic', 'content', 'created_at', 'updated_at')
    list_filter = ('user', 'comic', 'created_at')
