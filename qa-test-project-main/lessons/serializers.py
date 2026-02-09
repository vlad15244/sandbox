from rest_framework import serializers
from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'author', 'is_published', 'created_at']
        read_only_fields = ['author', 'created_at']
