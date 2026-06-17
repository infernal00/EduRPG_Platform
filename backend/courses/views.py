from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import UserProfile

from .models import Lesson, LessonProgress, Subject
from .serializers import LessonSerializer, SubjectSerializer


def get_demo_or_request_user(request):
    if request.user and request.user.is_authenticated:
        return request.user

    User = get_user_model()
    user, _ = User.objects.get_or_create(
        username="demo",
        defaults={"email": "demo@example.com"},
    )
    return user


@api_view(["GET"])
@permission_classes([AllowAny])
def subjects_list(request):
    subjects = Subject.objects.filter(is_active=True).prefetch_related(
        "topics__lessons",
        "topics__lessons__topic__subject",
    )
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def lessons_list(request):
    lessons = Lesson.objects.filter(is_active=True).select_related(
        "topic",
        "topic__subject",
    )

    subject_id = request.query_params.get("subject_id")
    topic_id = request.query_params.get("topic_id")

    if subject_id:
        lessons = lessons.filter(topic__subject_id=subject_id)

    if topic_id:
        lessons = lessons.filter(topic_id=topic_id)

    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def lesson_detail(request, pk):
    lesson = get_object_or_404(
        Lesson.objects.select_related("topic", "topic__subject"),
        pk=pk,
        is_active=True,
    )
    serializer = LessonSerializer(lesson)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def complete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk, is_active=True)
    user = get_demo_or_request_user(request)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    progress, _ = LessonProgress.objects.get_or_create(
        user=user,
        lesson=lesson,
        defaults={"is_completed": False},
    )

    if progress.is_completed:
        return Response(
            {
                "completed": True,
                "already_completed": True,
                "xp_earned": 0,
                "coins_earned": 0,
                "total_xp": profile.xp,
                "total_coins": profile.coins,
                "level": profile.level,
                "status": "already_completed",
                "lesson_id": lesson.id,
                "lesson_title": lesson.title,
                "xp_gained": 0,
                "coins_gained": 0,
            },
        )

    progress.complete()
    profile.add_rewards(lesson.xp_reward, lesson.coins_reward)

    return Response(
        {
            "completed": True,
            "already_completed": False,
            "xp_earned": lesson.xp_reward,
            "coins_earned": lesson.coins_reward,
            "total_xp": profile.xp,
            "total_coins": profile.coins,
            "level": profile.level,
            "status": "completed",
            "lesson_id": lesson.id,
            "lesson_title": lesson.title,
            "xp_gained": lesson.xp_reward,
            "coins_gained": lesson.coins_reward,
        },
    )
