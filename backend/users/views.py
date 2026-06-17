from django.db.models import Count, Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, LessonCompletion

from .models import UserProfile
from .serializers import (
    AchievementStatusSerializer,
    CurrentUserSerializer,
    LeaderboardEntrySerializer,
    RegisterSerializer,
    UserStatsSerializer,
)
from .services import achievements_for_user, get_profile


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "id": user.id,
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )


class CurrentUserView(APIView):
    def get(self, request):
        profile = get_profile(request.user)
        achievements = achievements_for_user(request.user)
        unlocked_count = sum(1 for achievement in achievements if achievement["unlocked"])
        course_progress = Course.objects.filter(is_active=True).aggregate(
            total_courses=Count("id", distinct=True),
            total_lessons=Count("lessons", filter=Q(lessons__is_active=True), distinct=True),
            completed_lessons=Count(
                "lessons__completions",
                filter=Q(
                    lessons__is_active=True,
                    lessons__completions__user=request.user,
                ),
                distinct=True,
            ),
        )
        data = {
            "user": request.user,
            "points": profile.points,
            "streak": profile.streak,
            "last_activity_date": profile.last_activity_date,
            "achievements": {
                "total": len(achievements),
                "unlocked": unlocked_count,
                "items": achievements,
            },
            "progress": {
                **course_progress,
                "completed_any_lessons": LessonCompletion.objects.filter(user=request.user).exists(),
            },
        }
        serializer = CurrentUserSerializer(data)
        return Response(serializer.data)


class AchievementsView(APIView):
    def get(self, request):
        data = achievements_for_user(request.user)
        serializer = AchievementStatusSerializer(data, many=True)
        return Response(serializer.data)


class LeaderboardView(APIView):
    def get(self, request):
        profiles = (
            UserProfile.objects.select_related("user")
            .order_by("-points", "-streak", "user__username")[:100]
        )
        serializer = LeaderboardEntrySerializer(profiles, many=True)
        return Response(serializer.data)


class StatsView(APIView):
    def get(self, request):
        profile = get_profile(request.user)
        serializer = UserStatsSerializer(profile)
        return Response(serializer.data)
