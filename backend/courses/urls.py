from django.urls import path

from .views import CourseLessonListView, CourseListView, LessonCompleteView, LessonListView

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="course-list"),
    path("courses/<int:course_id>/lessons/", CourseLessonListView.as_view(), name="course-lesson-list"),
    path("lessons/", LessonListView.as_view(), name="lesson-list"),
    path("lessons/<int:lesson_id>/complete/", LessonCompleteView.as_view(), name="lesson-complete"),
]
