from rest_framework import serializers

from .models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    completed_lessons = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "level",
            "xp",
            "coins",
            "completed_lessons",
        ]

    def get_completed_lessons(self, profile):
        return profile.user.lesson_progress.filter(is_completed=True).count()
