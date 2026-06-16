from django.urls import path

from .views import LessonCompleteView, LessonListView

urlpatterns = [
    path("lessons/", LessonListView.as_view(), name="lesson-list"),
    path("lessons/<int:lesson_id>/complete/", LessonCompleteView.as_view(), name="lesson-complete"),
]
