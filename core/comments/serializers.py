from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # hiển thị username

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']