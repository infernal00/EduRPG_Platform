from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Subject, Lesson
from .serializers import SubjectSerializer, LessonSerializer

@api_view(["GET"])
@permission_classes([AllowAny])
def api_home(request):
    return Response({
        "project": "EduRPG Platform",
        "status": "Backend is working",
        "version": "0.1.0",
        "endpoints": {
            "health": "/api/health/",
            "admin": "/admin/",
        },
        "modules": [
            "users",
            "subjects",
            "quests",
            "duels",
            "shop",
            "leaderboard",
        ],
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        "status": "ok",
        "service": "EduRPG backend",
        "version": "0.1.0",
    })

@api_view(["GET"])
@permission_classes([AllowAny])
def subjects_list(request):
    subjects = Subject.objects.filter(is_active=True).prefetch_related(
        "topics__lessons"
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