from django.urls import path

from .views import AchievementsView, CurrentUserView, LeaderboardView, RegisterView, StatsView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("achievements/", AchievementsView.as_view(), name="achievements"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path("stats/", StatsView.as_view(), name="stats"),
]
