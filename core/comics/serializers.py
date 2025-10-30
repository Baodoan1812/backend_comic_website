from rest_framework import serializers
from .models import Comic

class ComicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comic
        fields = ['id', 'title', 'description','read_count',  'cover_image', 'author', 'created_by', 'genre', 'created_at', 'updated_at']
