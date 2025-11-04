from rest_framework import serializers
from .models import Chapter

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'
        read_only_fields = ['comic', 'created_by', 'created_at', 'updated_at']