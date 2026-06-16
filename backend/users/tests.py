from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from courses.models import Lesson
from users.models import Achievement, UserAchievement


class GamificationAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="learner",
            password="pass12345",
        )
        self.client.force_authenticate(self.user)
        self.lesson = Lesson.objects.create(title="Intro", reward_points=40)

    def test_achievements_endpoint_returns_data(self):
        response = self.client.get(reverse("achievements"))

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 2)
        self.assertIn(
            {"name": "First Lesson", "unlocked": False},
            response.data,
        )

    def test_leaderboard_works_and_sorts_by_points(self):
        second_user = get_user_model().objects.create_user(
            username="runner_up",
            password="pass12345",
        )
        self.user.profile.points = 500
        self.user.profile.save(update_fields=["points"])
        second_user.profile.points = 400
        second_user.profile.save(update_fields=["points"])

        response = self.client.get(reverse("leaderboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["username"], "learner")
        self.assertEqual(response.data[0]["points"], 500)
        self.assertEqual(response.data[1]["username"], "runner_up")

    def test_streak_updates_after_lesson_completion(self):
        profile = self.user.profile
        profile.streak = 1
        profile.last_activity_date = timezone.localdate() - timedelta(days=1)
        profile.save(update_fields=["streak", "last_activity_date"])

        response = self.client.post(reverse("lesson-complete", args=[self.lesson.id]))

        self.assertEqual(response.status_code, 201)
        profile.refresh_from_db()
        self.assertEqual(profile.streak, 2)
        self.assertEqual(profile.points, 40)

    def test_first_lesson_achievement_unlocks_after_completion(self):
        response = self.client.post(reverse("lesson-complete", args=[self.lesson.id]))

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            UserAchievement.objects.filter(
                user=self.user,
                achievement__code=Achievement.FIRST_LESSON,
            ).exists()
        )

    def test_three_day_streak_achievement_unlocks_after_completion(self):
        profile = self.user.profile
        profile.streak = 2
        profile.last_activity_date = timezone.localdate() - timedelta(days=1)
        profile.save(update_fields=["streak", "last_activity_date"])

        response = self.client.post(reverse("lesson-complete", args=[self.lesson.id]))

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            UserAchievement.objects.filter(
                user=self.user,
                achievement__code=Achievement.THREE_DAY_STREAK,
            ).exists()
        )
