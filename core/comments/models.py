from django.db import models
from django.conf import settings

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comic = models.ForeignKey('comics.Comic', on_delete=models.CASCADE,null=True, blank=True, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{getattr(self.user, "username", "Unknown User")} - {self.content[:20] if self.content else ""}'
