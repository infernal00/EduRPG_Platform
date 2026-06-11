from django.urls import path
from .views import api_home, health_check

urlpatterns = [
    path("", api_home, name="api_home"),
    path("health/", health_check, name="health_check"),
]