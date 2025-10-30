from django.db import models
from django.conf import settings

class Comic(models.Model):
    title = models.CharField(max_length=255)
    author = models.TextField(max_length=255)
    description = models.TextField(blank=True)
    read_count = models.IntegerField(default=0)
    genre = models.CharField(max_length=100, blank=True)
    cover_image = models.ImageField(upload_to='comics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comics' )

    def __str__(self):
        return self.title
