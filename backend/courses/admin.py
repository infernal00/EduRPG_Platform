from django.contrib import admin

from .models import Lesson, LessonCompletion


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "reward_points")
    search_fields = ("title",)


@admin.register(LessonCompletion)
class LessonCompletionAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed_at")
    search_fields = ("user__username", "lesson__title")
