from django.urls import path

from .views import complete_lesson, lesson_detail, lessons_list, subjects_list

urlpatterns = [
    path("subjects/", subjects_list, name="subjects_list"),
    path("lessons/", lessons_list, name="lessons_list"),
    path("lessons/<int:pk>/", lesson_detail, name="lesson_detail"),
    path("lessons/<int:pk>/complete/", complete_lesson, name="complete_lesson"),
]
