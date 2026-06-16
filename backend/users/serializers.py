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
