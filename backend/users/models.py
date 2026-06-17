from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    points = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} profile"


class Achievement(models.Model):
    FIRST_LESSON = "first_lesson"
    THREE_DAY_STREAK = "three_day_streak"

    code = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_achievements",
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name="user_achievements",
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "achievement")
        ordering = ["-unlocked_at"]

    def __str__(self):
        return f"{self.user.username}: {self.achievement.name}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
