from django.conf import settings
from django.db import migrations
from django.utils import timezone


DEMO_USERS = [
    {
        "username": "edurpg_demo_champion",
        "email": "champion@example.com",
        "points": 250,
        "streak": 7,
    },
    {
        "username": "edurpg_demo_runner",
        "email": "runner@example.com",
        "points": 120,
        "streak": 3,
    },
]


def create_demo_leaderboard(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)
    UserProfile = apps.get_model("users", "UserProfile")

    for item in DEMO_USERS:
        user, _ = User.objects.update_or_create(
            username=item["username"],
            defaults={
                "email": item["email"],
                "is_active": True,
                "password": "!",
            },
        )
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "points": item["points"],
                "streak": item["streak"],
                "last_activity_date": timezone.localdate(),
            },
        )


def remove_demo_leaderboard(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)
    User.objects.filter(username__in=[item["username"] for item in DEMO_USERS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_demo_achievements"),
    ]

    operations = [
        migrations.RunPython(create_demo_leaderboard, remove_demo_leaderboard),
    ]
