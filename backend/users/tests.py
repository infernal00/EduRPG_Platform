from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from courses.models import Lesson, LessonCompletion
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

    def test_leaderboard_sorts_by_points_streak_and_username(self):
        users = [
            get_user_model().objects.create_user(username="charlie", password="pass12345"),
            get_user_model().objects.create_user(username="bravo", password="pass12345"),
            get_user_model().objects.create_user(username="alpha", password="pass12345"),
        ]
        scores = {
            "charlie": (100, 1),
            "bravo": (100, 3),
            "alpha": (100, 3),
        }
        for user in users:
            points, streak = scores[user.username]
            user.profile.points = points
            user.profile.streak = streak
            user.profile.save(update_fields=["points", "streak"])
        self.user.profile.points = 50
        self.user.profile.streak = 10
        self.user.profile.save(update_fields=["points", "streak"])

        response = self.client.get(reverse("leaderboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [entry["username"] for entry in response.data[:4]],
            ["alpha", "bravo", "charlie", "learner"],
        )

    def test_leaderboard_can_be_empty(self):
        get_user_model().objects.all().delete()

        response = self.client.get(reverse("leaderboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

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

    def test_streak_resets_after_missed_day(self):
        profile = self.user.profile
        profile.streak = 5
        profile.last_activity_date = timezone.localdate() - timedelta(days=2)
        profile.save(update_fields=["streak", "last_activity_date"])

        response = self.client.post(reverse("lesson-complete", args=[self.lesson.id]))

        self.assertEqual(response.status_code, 201)
        profile.refresh_from_db()
        self.assertEqual(profile.streak, 1)

    def test_multiple_lessons_on_same_day_do_not_increase_streak_twice(self):
        second_lesson = Lesson.objects.create(title="Follow up", reward_points=30)

        first_response = self.client.post(reverse("lesson-complete", args=[self.lesson.id]))
        second_response = self.client.post(reverse("lesson-complete", args=[second_lesson.id]))

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 201)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.streak, 1)
        self.assertEqual(self.user.profile.points, 70)

    def test_repeating_lesson_completion_is_idempotent_for_points_and_streak(self):
        first_response = self.client.post(reverse("lesson-complete", args=[self.lesson.id]))
        second_response = self.client.post(reverse("lesson-complete", args=[self.lesson.id]))

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 200)
        self.assertFalse(second_response.data["created"])
        self.assertEqual(LessonCompletion.objects.filter(user=self.user, lesson=self.lesson).count(), 1)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.points, 40)
        self.assertEqual(self.user.profile.streak, 1)

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

    def test_new_user_has_empty_stats_and_locked_achievements(self):
        response = self.client.get(reverse("stats"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "username": "learner",
                "points": 0,
                "streak": 0,
            },
        )

        achievements_response = self.client.get(reverse("achievements"))

        self.assertEqual(achievements_response.status_code, 200)
        self.assertTrue(achievements_response.data)
        self.assertTrue(all(not item["unlocked"] for item in achievements_response.data))
