from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Users
from .serializers import UsersSerializer, CustomTokenObtainPairSerializer

# 1. Кастомный View для входа (получения токена)
class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# 2. Обновленный ViewSet пользователей
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    
    def get_permissions(self):
        """
        Динамически управляем правами доступа:
        Регистрация доступна всем, а просмотр списка пользователей — только по JWT токену.
        """
        if self.action in ['register', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'message': 'Пользователь успешно зарегистрирован', 'user': serializer.data}, 
            status=status.HTTP_201_CREATED
        )