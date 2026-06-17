from django.db import migrations


DEMO_ACHIEVEMENTS = [
    {
        "code": "first_lesson",
        "name": "First Lesson",
        "description": "Complete your first lesson.",
    },
    {
        "code": "three_day_streak",
        "name": "3 Day Streak",
        "description": "Keep learning for three active days in a row.",
    },
]


def create_demo_achievements(apps, schema_editor):
    Achievement = apps.get_model("users", "Achievement")
    for achievement in DEMO_ACHIEVEMENTS:
        Achievement.objects.update_or_create(
            code=achievement["code"],
            defaults={
                "name": achievement["name"],
                "description": achievement["description"],
            },
        )


def remove_demo_achievements(apps, schema_editor):
    Achievement = apps.get_model("users", "Achievement")
    Achievement.objects.filter(code__in=[item["code"] for item in DEMO_ACHIEVEMENTS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_demo_achievements, remove_demo_achievements),
    ]
