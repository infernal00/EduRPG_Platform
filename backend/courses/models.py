from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=80, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=40, blank=True)
    theme = models.CharField(max_length=40, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    DIFFICULTY_CHOICES = [
        (EASY, "Easy"),
        (MEDIUM, "Medium"),
        (HARD, "Hard"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default=EASY)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    reward_points = models.PositiveIntegerField(default=30)

    class Meta:
        ordering = ["course__order", "order", "id"]
        unique_together = ("course", "slug")

    def __str__(self):
        return self.title


class LessonCompletion(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_completions",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="completions",
    )
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "lesson")
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.user.username}: {self.lesson.title}"
