from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Category, Lesson, UserLessonProgress,
    Test, Question, TestAttempt,
    FlashcardDeck, Flashcard,
    Battle, BattleParticipant,
    Achievement, UserAchievement,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'level', 'xp', 'coins', 'streak_days', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('RPG Stats', {'fields': ('level', 'xp', 'xp_to_next_level', 'coins', 'total_xp_earned',
                                  'lessons_completed', 'tests_completed', 'battles_won',
                                  'battles_played', 'streak_days', 'last_activity', 'avatar_url')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'xp_reward', 'is_published')
    list_filter = ('difficulty', 'is_published', 'category')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'pass_score', 'xp_reward', 'is_published')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'correct_answer')


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'passed', 'created_at')


@admin.register(FlashcardDeck)
class FlashcardDeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published')


@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'winner', 'created_at')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'xp_reward', 'coin_reward')


admin.site.register(Flashcard)
admin.site.register(BattleParticipant)
admin.site.register(UserAchievement)
admin.site.register(UserLessonProgress)
