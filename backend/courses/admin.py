from django.contrib import admin

from .models import Course, Lesson, LessonCompletion


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "order", "is_active")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "difficulty", "order", "reward_points", "is_active")
    list_filter = ("course", "difficulty", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description", "content")


@admin.register(LessonCompletion)
class LessonCompletionAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed_at")
    search_fields = ("user__username", "lesson__title")
