from datetime import timedelta

from django.apps import apps
from django.utils import timezone

from .models import Achievement, UserAchievement, UserProfile


def get_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def update_streak(user, activity_date=None):
    activity_date = activity_date or timezone.localdate()
    profile = get_profile(user)

    if profile.last_activity_date == activity_date:
        return profile

    if profile.last_activity_date == activity_date - timedelta(days=1):
        profile.streak += 1
    else:
        profile.streak = 1

    profile.last_activity_date = activity_date
    profile.save(update_fields=["streak", "last_activity_date"])
    return profile


def award_lesson_completion(user, lesson):
    profile = update_streak(user)
    profile.points += lesson.reward_points
    profile.save(update_fields=["points"])
    unlock_achievements(user)
    return profile


def unlock_achievements(user):
    LessonCompletion = apps.get_model("courses", "LessonCompletion")
    profile = get_profile(user)
    completed_lessons = LessonCompletion.objects.filter(user=user).count()
    unlocked_codes = set(
        UserAchievement.objects.filter(user=user).values_list("achievement__code", flat=True)
    )

    codes_to_unlock = []
    if completed_lessons >= 1:
        codes_to_unlock.append(Achievement.FIRST_LESSON)
    if profile.streak >= 3:
        codes_to_unlock.append(Achievement.THREE_DAY_STREAK)

    achievements = Achievement.objects.filter(code__in=codes_to_unlock)
    for achievement in achievements:
        if achievement.code not in unlocked_codes:
            UserAchievement.objects.get_or_create(user=user, achievement=achievement)


def achievements_for_user(user):
    unlocked_ids = set(
        UserAchievement.objects.filter(user=user).values_list("achievement_id", flat=True)
    )
    return [
        {
            "name": achievement.name,
            "unlocked": achievement.id in unlocked_ids,
        }
        for achievement in Achievement.objects.all()
    ]
