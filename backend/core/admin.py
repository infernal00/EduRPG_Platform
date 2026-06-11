from django.contrib import admin

from .models import Subject, Topic, Lesson


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subject", "order")
    search_fields = ("title", "subject__name")
    list_filter = ("subject",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "topic",
        "level",
        "xp_reward",
        "coins_reward",
        "is_active",
        "order",
    )
    search_fields = ("title", "topic__title", "topic__subject__name")
    list_filter = ("level", "is_active", "topic__subject")