from django.conf import settings
from django.db import models
from django.utils import timezone


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.ForeignKey(
        Subject,
        related_name="topics",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["subject", "order", "title"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    LEVEL_BEGINNER = "beginner"
    LEVEL_ADVANCED = "advanced"
    LEVEL_EXPERT = "expert"

    LEVEL_CHOICES = [
        (LEVEL_BEGINNER, "Beginner"),
        (LEVEL_ADVANCED, "Advanced"),
        (LEVEL_EXPERT, "Expert"),
    ]

    topic = models.ForeignKey(
        Topic,
        related_name="lessons",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default=LEVEL_BEGINNER,
    )
    xp_reward = models.PositiveIntegerField(default=30)
    coins_reward = models.PositiveIntegerField(default=15)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["topic", "order", "title"]

    def __str__(self):
        return self.title


class LessonProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="lesson_progress",
        on_delete=models.CASCADE,
    )
    lesson = models.ForeignKey(
        Lesson,
        related_name="progress_records",
        on_delete=models.CASCADE,
    )
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "lesson")

    def complete(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
