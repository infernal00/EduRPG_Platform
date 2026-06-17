from django.contrib.auth import get_user_model
from rest_framework import serializers


class AchievementStatusSerializer(serializers.Serializer):
    name = serializers.CharField()
    unlocked = serializers.BooleanField()


class LeaderboardEntrySerializer(serializers.Serializer):
    username = serializers.CharField(source="user.username")
    points = serializers.IntegerField()
    streak = serializers.IntegerField()


class UserStatsSerializer(serializers.Serializer):
    username = serializers.CharField(source="user.username")
    points = serializers.IntegerField()
    streak = serializers.IntegerField()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class CurrentUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    points = serializers.IntegerField()
    streak = serializers.IntegerField()
    last_activity_date = serializers.DateField(allow_null=True)
    achievements = serializers.DictField()
    progress = serializers.DictField()
