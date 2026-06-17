from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import UserProfile
from .serializers import ProfileSerializer


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
def profile_detail(request):
    user = get_demo_or_request_user(request)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)
