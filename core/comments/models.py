from django.db import models
from django.conf import settings

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # tự động cập nhật khi edit

    def __str__(self):
        return f'{self.user.username} - {self.content[:20]}'