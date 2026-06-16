from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UsersViewSet, CustomTokenObtainView

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    
    # Эндпоинты для JWT
    path('auth/login/', CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]