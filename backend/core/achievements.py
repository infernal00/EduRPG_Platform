from .models import Achievement, UserAchievement

ACHIEVEMENTS_DATA = [
    {"code": "first_lesson",  "title": "Первый шаг",       "description": "Пройди свой первый урок",      "icon": "📚", "xp_reward": 20,  "coin_reward": 10},
    {"code": "lesson_5",      "title": "Прилежный ученик", "description": "Пройди 5 уроков",              "icon": "🎓", "xp_reward": 50,  "coin_reward": 25},
    {"code": "lesson_20",     "title": "Знаток",           "description": "Пройди 20 уроков",             "icon": "🏆", "xp_reward": 150, "coin_reward": 75},
    {"code": "first_test",    "title": "Первый экзамен",   "description": "Сдай свой первый тест",        "icon": "📝", "xp_reward": 20,  "coin_reward": 10},
    {"code": "perfect_test",  "title": "Отличник",         "description": "Получи 100% в тесте",          "icon": "⭐", "xp_reward": 75,  "coin_reward": 50},
    {"code": "test_5",        "title": "Тестировщик",      "description": "Пройди 5 тестов",              "icon": "✅", "xp_reward": 50,  "coin_reward": 25},
    {"code": "first_battle",  "title": "Боевое крещение",  "description": "Прими участие в первом батле", "icon": "⚔️", "xp_reward": 30,  "coin_reward": 15},
    {"code": "battle_win_1",  "title": "Победитель",       "description": "Выиграй свой первый батл",     "icon": "🥇", "xp_reward": 60,  "coin_reward": 40},
    {"code": "battle_win_10", "title": "Чемпион",          "description": "Выиграй 10 батлов",            "icon": "👑", "xp_reward": 200, "coin_reward": 100},
    {"code": "streak_7",      "title": "Неделя подряд",    "description": "Учись 7 дней подряд",          "icon": "🔥", "xp_reward": 100, "coin_reward": 50},
    {"code": "streak_30",     "title": "Месяц усердия",    "description": "Учись 30 дней подряд",         "icon": "💎", "xp_reward": 500, "coin_reward": 200},
    {"code": "level_5",       "title": "Опытный",          "description": "Достигни 5 уровня",            "icon": "🌟", "xp_reward": 0,   "coin_reward": 50},
    {"code": "level_10",      "title": "Ветеран",          "description": "Достигни 10 уровня",           "icon": "🚀", "xp_reward": 0,   "coin_reward": 150},
    {"code": "rich",          "title": "Богач",            "description": "Накопи 500 монет",             "icon": "💰", "xp_reward": 30,  "coin_reward": 0},
]


def seed_achievements():
    for data in ACHIEVEMENTS_DATA:
        Achievement.objects.get_or_create(code=data['code'], defaults=data)


def check_and_grant(user):
    """Проверить все достижения и выдать незаработанные."""
    earned = set(user.achievements.values_list('achievement__code', flat=True))
    newly_earned = []

    checks = {
        "first_lesson":  user.lessons_completed >= 1,
        "lesson_5":      user.lessons_completed >= 5,
        "lesson_20":     user.lessons_completed >= 20,
        "first_test":    user.tests_completed >= 1,
        "test_5":        user.tests_completed >= 5,
        "first_battle":  user.battles_played >= 1,
        "battle_win_1":  user.battles_won >= 1,
        "battle_win_10": user.battles_won >= 10,
        "streak_7":      user.streak_days >= 7,
        "streak_30":     user.streak_days >= 30,
        "level_5":       user.level >= 5,
        "level_10":      user.level >= 10,
        "rich":          user.coins >= 500,
    }

    for code, condition in checks.items():
        if condition and code not in earned:
            try:
                achievement = Achievement.objects.get(code=code)
                UserAchievement.objects.create(user=user, achievement=achievement)
                if achievement.xp_reward or achievement.coin_reward:
                    user.award(xp=achievement.xp_reward, coins=achievement.coin_reward)
                newly_earned.append(code)
            except Achievement.DoesNotExist:
                pass

    return newly_earned
