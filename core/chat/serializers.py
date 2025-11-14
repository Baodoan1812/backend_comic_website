from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # hiển thị username

    class Meta:
        model = Chat
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']
