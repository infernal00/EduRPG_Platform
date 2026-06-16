from django.urls import path

from .views import AchievementsView, LeaderboardView, StatsView

urlpatterns = [
    path("achievements/", AchievementsView.as_view(), name="achievements"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path("stats/", StatsView.as_view(), name="stats"),
]
