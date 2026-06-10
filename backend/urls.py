from django.urls import path
from . import views

urlpatterns = [
    # Health
    path('', views.api_home, name='api_home'),

    # Auth
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),

    # Users
    path('users/me/', views.me, name='me'),
    path('users/me/achievements/', views.my_achievements, name='my_achievements'),
    path('users/leaderboard/', views.leaderboard, name='leaderboard'),

    # Categories
    path('categories/', views.categories, name='categories'),

    # Lessons
    path('lessons/', views.lessons_list, name='lessons_list'),
    path('lessons/progress/', views.my_lesson_progress, name='my_lesson_progress'),
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:pk>/complete/', views.complete_lesson, name='complete_lesson'),

    # Tests
    path('tests/', views.tests_list, name='tests_list'),
    path('tests/attempts/', views.my_test_attempts, name='my_test_attempts'),
    path('tests/<int:pk>/', views.test_detail, name='test_detail'),
    path('tests/<int:pk>/submit/', views.submit_test, name='submit_test'),

    # Flashcards
    path('flashcards/', views.flashcard_decks, name='flashcard_decks'),
    path('flashcards/<int:pk>/', views.flashcard_deck_detail, name='flashcard_deck_detail'),

    # Battles
    path('battles/', views.battles_list, name='battles_list'),
    path('battles/<int:pk>/', views.battle_detail, name='battle_detail'),
    path('battles/<int:pk>/join/', views.battle_join, name='battle_join'),
    path('battles/<int:pk>/answer/', views.battle_answer, name='battle_answer'),
    path('battles/<int:pk>/finish/', views.battle_finish, name='battle_finish'),
]
