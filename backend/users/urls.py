from django.urls import path

from .views import profile_detail

urlpatterns = [
    path("profile/", profile_detail, name="profile_detail"),
]
