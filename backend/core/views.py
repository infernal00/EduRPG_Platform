from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


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