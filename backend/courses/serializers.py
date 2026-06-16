from rest_framework import serializers

from .models import Lesson, LessonCompletion


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "reward_points"]


class LessonCompletionSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = LessonCompletion
        fields = ["id", "lesson", "completed_at"]
