from django.contrib import admin
from .models import Comic
@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'created_by', 'read_count','genre')  
    search_fields = ('title', 'author')                      
    list_filter = ('author',)   