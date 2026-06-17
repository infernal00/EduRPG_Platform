from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Course, Lesson, LessonCompletion


class CourseAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="learner",
            password="pass12345",
        )
        self.course = Course.objects.create(
            title="Algebra Tower",
            slug="algebra-tower-test",
            description="Equations and variables.",
            icon="sigma",
            theme="indigo",
            order=2,
        )
        self.first_lesson = Lesson.objects.create(
            course=self.course,
            title="Variables",
            slug="variables",
            order=1,
            reward_points=35,
        )
        self.second_lesson = Lesson.objects.create(
            course=self.course,
            title="Linear equations",
            slug="linear-equations",
            order=2,
            reward_points=45,
        )

    def test_course_list_requires_authentication(self):
        response = self.client.get(reverse("course-list"))

        self.assertEqual(response.status_code, 401)

    def test_course_list_returns_lesson_and_completion_counts(self):
        self.client.force_authenticate(self.user)
        LessonCompletion.objects.create(user=self.user, lesson=self.first_lesson)

        response = self.client.get(reverse("course-list"))

        self.assertEqual(response.status_code, 200)
        course = next(item for item in response.data if item["id"] == self.course.id)
        self.assertEqual(course["lessons_count"], 2)
        self.assertEqual(course["completed_count"], 1)
        self.assertEqual(course["slug"], "algebra-tower-test")

    def test_course_lessons_return_in_order_with_user_progress(self):
        self.client.force_authenticate(self.user)
        LessonCompletion.objects.create(user=self.user, lesson=self.second_lesson)

        response = self.client.get(reverse("course-lesson-list", args=[self.course.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual([lesson["slug"] for lesson in response.data], ["variables", "linear-equations"])
        self.assertFalse(response.data[0]["completed"])
        self.assertIsNone(response.data[0]["completed_at"])
        self.assertTrue(response.data[1]["completed"])
        self.assertIsNotNone(response.data[1]["completed_at"])
