from django.shortcuts import get_object_or_404
from django.db.models import Count, Exists, OuterRef, Q, Subquery
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services import award_lesson_completion, get_profile, unlock_achievements

from .models import Course, Lesson, LessonCompletion
from .serializers import CourseSerializer, LessonCompletionSerializer, LessonSerializer


def lessons_with_user_progress(user):
    completions = LessonCompletion.objects.filter(user=user, lesson=OuterRef("pk"))
    return (
        Lesson.objects.filter(is_active=True)
        .select_related("course")
        .annotate(
            completed=Exists(completions),
            completed_at=Subquery(completions.values("completed_at")[:1]),
        )
    )


class CourseListView(APIView):
    def get(self, request):
        courses = (
            Course.objects.filter(is_active=True)
            .annotate(
                lessons_count=Count("lessons", filter=Q(lessons__is_active=True)),
                completed_count=Count(
                    "lessons__completions",
                    filter=Q(
                        lessons__is_active=True,
                        lessons__completions__user=request.user,
                    ),
                    distinct=True,
                ),
            )
            .order_by("order", "id")
        )
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseLessonListView(APIView):
    def get(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id, is_active=True)
        lessons = lessons_with_user_progress(request.user).filter(course=course)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class LessonListView(APIView):
    def get(self, request):
        serializer = LessonSerializer(lessons_with_user_progress(request.user), many=True)
        return Response(serializer.data)


class LessonCompleteView(APIView):
    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        completion, created = LessonCompletion.objects.get_or_create(
            user=request.user,
            lesson=lesson,
        )

        if created:
            profile = award_lesson_completion(request.user, lesson)
        else:
            unlock_achievements(request.user)
            profile = get_profile(request.user)

        serializer = LessonCompletionSerializer(completion)
        return Response(
            {
                "completion": serializer.data,
                "created": created,
                "points": profile.points,
                "streak": profile.streak,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
