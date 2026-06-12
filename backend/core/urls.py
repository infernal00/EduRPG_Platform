from django.urls import path

from .views import (
    api_home,
    health_check,
    subjects_list,
    lessons_list,
    lesson_detail,
    complete_lesson,
)

urlpatterns = [
    path("", api_home, name="api_home"),
    path("health/", health_check, name="health_check"),
    path("subjects/", subjects_list, name="subjects_list"),
    path("lessons/", lessons_list, name="lessons_list"),
    path("lessons/<int:pk>/", lesson_detail, name="lesson_detail"),
    path("lessons/<int:pk>/complete/", complete_lesson, name="complete_lesson"),
]