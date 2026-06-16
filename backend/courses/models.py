from django.conf import settings
from django.db import models


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reward_points = models.PositiveIntegerField(default=30)

    class Meta:
        ordering = ["id"]

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
