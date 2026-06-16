from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services import award_lesson_completion, get_profile, unlock_achievements

from .models import Lesson, LessonCompletion
from .serializers import LessonCompletionSerializer, LessonSerializer


class LessonListView(APIView):
    def get(self, request):
        serializer = LessonSerializer(Lesson.objects.all(), many=True)
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
