from rest_framework import serializers

from .models import Course, Lesson, LessonCompletion


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(read_only=True)
    completed_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "icon",
            "theme",
            "order",
            "lessons_count",
            "completed_count",
        ]


class LessonSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(source="course.id", read_only=True)
    completed = serializers.BooleanField(read_only=True, default=False)
    completed_at = serializers.DateTimeField(read_only=True, allow_null=True)

    class Meta:
        model = Lesson
        fields = [
            "id",
            "course_id",
            "title",
            "slug",
            "description",
            "content",
            "difficulty",
            "order",
            "reward_points",
            "completed",
            "completed_at",
        ]


class LessonCompletionSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = LessonCompletion
        fields = ["id", "lesson", "completed_at"]
