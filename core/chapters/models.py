from django.db import models
from django.conf import settings

class Chapter(models.Model):
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chapters/', blank=True, null=True)
    comic = models.ForeignKey('comics.Comic', on_delete=models.CASCADE, related_name='chapters')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chapters'
    )

    def __str__(self):
        return f"Chapter {self.number}: {self.title}"