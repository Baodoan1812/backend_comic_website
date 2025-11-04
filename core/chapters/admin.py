from django.contrib import admin
from .models import Chapter

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'title', 'comic','image', 'created_by', 'created_at')
    list_filter = ('comic', 'created_by', 'created_at')
    search_fields = ('title', 'comic__title')
    ordering = ('comic', 'number')
