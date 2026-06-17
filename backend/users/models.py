from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE,
    )
    xp = models.PositiveIntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def add_rewards(self, xp_amount, coins_amount):
        self.xp += xp_amount
        self.coins += coins_amount
        self.level = self.xp // 100 + 1
        self.save()

    def __str__(self):
        return f"{self.user.username} profile"
