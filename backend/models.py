from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings as django_settings


# ─── Пользователь с RPG-статами ──────────────────────────────────────────────

class User(AbstractUser):
    avatar_url = models.URLField(blank=True, null=True)

    # RPG stats
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    xp_to_next_level = models.PositiveIntegerField(default=100)
    coins = models.PositiveIntegerField(default=0)
    total_xp_earned = models.PositiveIntegerField(default=0)
    lessons_completed = models.PositiveIntegerField(default=0)
    tests_completed = models.PositiveIntegerField(default=0)
    battles_won = models.PositiveIntegerField(default=0)
    battles_played = models.PositiveIntegerField(default=0)
    streak_days = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

    def xp_to_reach_level(self, level):
        base = django_settings.RPG_BASE_XP_PER_LEVEL
        mult = django_settings.RPG_XP_MULTIPLIER
        return int(base * (mult ** (level - 1)))

    def award(self, xp=0, coins=0):
        """Начислить XP и монеты, обработать level-up."""
        from django.utils import timezone
        import datetime

        leveled_up = False
        old_level = self.level

        self.xp += xp
        self.coins += coins
        self.total_xp_earned += xp

        # Level-up loop
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = self.xp_to_reach_level(self.level)
            leveled_up = True

        # Streak
        today = timezone.now().date()
        if self.last_activity:
            delta = (today - self.last_activity.date()).days
            if delta == 1:
                self.streak_days += 1
            elif delta > 1:
                self.streak_days = 1
        else:
            self.streak_days = 1

        self.last_activity = timezone.now()
        self.save()

        return {
            'xp_earned': xp,
            'coins_earned': coins,
            'leveled_up': leveled_up,
            'new_level': self.level,
            'old_level': old_level,
            'current_xp': self.xp,
            'xp_to_next_level': self.xp_to_next_level,
        }


# ─── Категория ───────────────────────────────────────────────────────────────

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


# ─── Урок ─────────────────────────────────────────────────────────────────────

class Lesson(models.Model):
    DIFFICULTY = [('easy', 'Легко'), ('medium', 'Средне'), ('hard', 'Сложно')]

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='lessons')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, default='easy')
    xp_reward = models.PositiveIntegerField(default=30)
    coin_reward = models.PositiveIntegerField(default=15)
    order_index = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lessons'
        ordering = ['order_index']

    def __str__(self):
        return self.title


class UserLessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent_seconds = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'user_lesson_progress'
        unique_together = ('user', 'lesson')


# ─── Тест ─────────────────────────────────────────────────────────────────────

class Test(models.Model):
    DIFFICULTY = [('easy', 'Легко'), ('medium', 'Средне'), ('hard', 'Сложно')]

    lesson = models.OneToOneField(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='test')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, default='medium')
    time_limit_seconds = models.PositiveIntegerField(null=True, blank=True)
    pass_score = models.PositiveIntegerField(default=70)  # % для зачёта
    xp_reward = models.PositiveIntegerField(default=50)
    coin_reward = models.PositiveIntegerField(default=25)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tests'

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    correct_answer = models.CharField(max_length=1)  # 'a', 'b', 'c', 'd'
    explanation = models.TextField(blank=True)
    order_index = models.PositiveIntegerField(default=0)
    xp_reward = models.PositiveIntegerField(default=10)
    coin_reward = models.PositiveIntegerField(default=5)

    class Meta:
        db_table = 'questions'
        ordering = ['order_index']

    def __str__(self):
        return self.text[:60]


class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    xp_earned = models.PositiveIntegerField(default=0)
    coins_earned = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    time_spent_seconds = models.PositiveIntegerField(default=0)
    answers = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'test_attempts'
        ordering = ['-created_at']


# ─── Карточки ─────────────────────────────────────────────────────────────────

class FlashcardDeck(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='decks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flashcard_decks'

    def __str__(self):
        return self.title


class Flashcard(models.Model):
    CARD_TYPES = [('term', 'Термин'), ('fact', 'Факт'), ('formula', 'Формула')]

    deck = models.ForeignKey(FlashcardDeck, on_delete=models.CASCADE, related_name='cards')
    card_type = models.CharField(max_length=10, choices=CARD_TYPES, default='term')
    front = models.TextField()
    back = models.TextField()
    hint = models.TextField(blank=True)
    order_index = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'flashcards'
        ordering = ['order_index']


# ─── Батл ─────────────────────────────────────────────────────────────────────

class Battle(models.Model):
    STATUS = [
        ('waiting', 'Ожидание'),
        ('in_progress', 'В процессе'),
        ('finished', 'Завершён'),
    ]

    status = models.CharField(max_length=15, choices=STATUS, default='waiting')
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, blank=True, related_name='battles')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_battles')
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'battles'
        ordering = ['-created_at']

    def __str__(self):
        return f"Battle #{self.id} [{self.status}]"


class BattleParticipant(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='battle_participations')
    score = models.PositiveIntegerField(default=0)
    answers = models.JSONField(default=dict)
    is_ready = models.BooleanField(default=True)
    xp_earned = models.PositiveIntegerField(default=0)
    coins_earned = models.PositiveIntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'battle_participants'
        unique_together = ('battle', 'user')


# ─── Достижения ───────────────────────────────────────────────────────────────

class Achievement(models.Model):
    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)
    xp_reward = models.PositiveIntegerField(default=0)
    coin_reward = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'achievements'

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_achievements'
        unique_together = ('user', 'achievement')
