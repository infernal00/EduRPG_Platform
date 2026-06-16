from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import (
    AchievementStatusSerializer,
    LeaderboardEntrySerializer,
    UserStatsSerializer,
)
from .services import achievements_for_user, get_profile


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
