from django.contrib import admin
from django.urls import include, path

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def api_home(request):
    return Response(
        {
            "project": "EduRPG Platform",
            "status": "Backend is working",
            "version": "0.1.0",
            "endpoints": {
                "health": "/api/health/",
                "profile": "/api/profile/",
                "subjects": "/api/subjects/",
                "lessons": "/api/lessons/",
                "admin": "/admin/",
            },
        },
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response(
        {
            "status": "ok",
            "service": "EduRPG backend",
            "version": "0.1.0",
        },
    )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_home, name="api_home"),
    path("api/health/", health_check, name="health_check"),
    path("api/", include("courses.urls")),
    path("api/", include("users.urls")),
]
