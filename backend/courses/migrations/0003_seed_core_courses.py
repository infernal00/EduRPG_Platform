from django.db import migrations


COURSES = [
    {
        "slug": "arithmetic-island",
        "title": "Остров арифметики",
        "description": "Базовые вычисления, порядок действий и уверенный старт в математике.",
        "icon": "calculator",
        "theme": "emerald",
        "order": 1,
        "lessons": [
            {
                "slug": "numbers-and-operations",
                "title": "Числа и операции",
                "description": "Повторяем сложение, вычитание, умножение и деление.",
                "content": "Решай короткие задания и следи за порядком действий.",
                "difficulty": "easy",
                "order": 1,
                "reward_points": 30,
            },
            {
                "slug": "fractions-basics",
                "title": "Основы дробей",
                "description": "Учимся читать, сравнивать и складывать простые дроби.",
                "content": "Дробь показывает часть целого. Начни с числителя и знаменателя.",
                "difficulty": "medium",
                "order": 2,
                "reward_points": 40,
            },
        ],
    },
    {
        "slug": "algebra-tower",
        "title": "Башня алгебры",
        "description": "Уравнения, переменные и первые формулы.",
        "icon": "sigma",
        "theme": "indigo",
        "order": 2,
        "lessons": [
            {
                "slug": "variables",
                "title": "Что такое переменная",
                "description": "Разбираем, зачем нужны x, y и другие неизвестные.",
                "content": "Переменная хранит неизвестное значение, которое можно найти из условий.",
                "difficulty": "easy",
                "order": 1,
                "reward_points": 35,
            },
            {
                "slug": "linear-equations",
                "title": "Линейные уравнения",
                "description": "Решаем уравнения вида ax + b = c.",
                "content": "Переноси известные части по сторонам и сохраняй равенство.",
                "difficulty": "medium",
                "order": 2,
                "reward_points": 45,
            },
        ],
    },
    {
        "slug": "programming-valley",
        "title": "Долина программирования",
        "description": "Логика, алгоритмы и первые шаги в коде.",
        "icon": "code",
        "theme": "amber",
        "order": 3,
        "lessons": [
            {
                "slug": "algorithm-steps",
                "title": "Шаги алгоритма",
                "description": "Учимся разбивать задачу на понятные инструкции.",
                "content": "Алгоритм должен быть точным, конечным и понятным исполнителю.",
                "difficulty": "easy",
                "order": 1,
                "reward_points": 30,
            },
            {
                "slug": "conditions",
                "title": "Условия",
                "description": "Используем ветвления, чтобы программа принимала решения.",
                "content": "Условие отвечает на вопрос да/нет и выбирает следующий шаг.",
                "difficulty": "medium",
                "order": 2,
                "reward_points": 40,
            },
        ],
    },
]


def seed_courses(apps, schema_editor):
    Course = apps.get_model("courses", "Course")
    Lesson = apps.get_model("courses", "Lesson")

    for course_data in COURSES:
        lessons = course_data["lessons"]
        course_defaults = {
            key: value for key, value in course_data.items() if key != "lessons"
        }
        course, _ = Course.objects.update_or_create(
            slug=course_data["slug"],
            defaults=course_defaults,
        )
        for lesson_data in lessons:
            Lesson.objects.update_or_create(
                course=course,
                slug=lesson_data["slug"],
                defaults=lesson_data,
            )


def remove_seed_courses(apps, schema_editor):
    Course = apps.get_model("courses", "Course")
    Course.objects.filter(slug__in=[course["slug"] for course in COURSES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0002_course_alter_lesson_options_lesson_content_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_courses, remove_seed_courses),
    ]
