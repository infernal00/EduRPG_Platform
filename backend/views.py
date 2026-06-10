from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Category, Lesson, UserLessonProgress, Test, Question,
    TestAttempt, FlashcardDeck, Flashcard, Battle, BattleParticipant,
    Achievement, UserAchievement,
)
from .serializers import (
    RegisterSerializer, UserProfileSerializer, UserUpdateSerializer,
    UserAchievementSerializer, LeaderboardSerializer,
    CategorySerializer, LessonSerializer, LessonDetailSerializer, LessonProgressSerializer,
    TestSerializer, TestDetailSerializer, TestAttemptSerializer,
    FlashcardDeckSerializer, FlashcardDeckDetailSerializer,
    BattleSerializer, AchievementSerializer,
)
from .achievements import check_and_grant, seed_achievements

User = get_user_model()


# ─── Health ───────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def api_home(request):
    return Response({
        'project': 'EduRPG Platform',
        'status': 'Backend is working ✅',
        'version': '1.0.0',
        'endpoints': {
            'auth': ['/api/auth/register/', '/api/auth/login/', '/api/auth/refresh/'],
            'users': ['/api/users/me/', '/api/users/leaderboard/'],
            'lessons': ['/api/lessons/', '/api/lessons/{id}/'],
            'tests': ['/api/tests/', '/api/tests/{id}/submit/'],
            'flashcards': ['/api/flashcards/'],
            'battles': ['/api/battles/', '/api/battles/{id}/join/'],
        }
    })


# ─── Auth ─────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        seed_achievements()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserProfileSerializer(user).data,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    from django.contrib.auth import authenticate
    email = request.data.get('email', '')
    password = request.data.get('password', '')

    try:
        user_obj = User.objects.get(email=email)
        username = user_obj.username
    except User.DoesNotExist:
        return Response({'detail': 'Неверный email или пароль'}, status=401)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'detail': 'Неверный email или пароль'}, status=401)

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserProfileSerializer(user).data,
    })


# ─── Users ────────────────────────────────────────────────────────────────────

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def me(request):
    if request.method == 'GET':
        return Response(UserProfileSerializer(request.user).data)

    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(UserProfileSerializer(request.user).data)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_achievements(request):
    items = UserAchievement.objects.filter(user=request.user).select_related('achievement')
    return Response(UserAchievementSerializer(items, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard(request):
    limit = int(request.query_params.get('limit', 20))
    users = User.objects.filter(is_active=True).order_by('-total_xp_earned')[:limit]
    data = []
    for idx, u in enumerate(users):
        row = LeaderboardSerializer(u).data
        row['rank'] = idx + 1
        data.append(row)
    return Response(data)


# ─── Categories ───────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def categories(request):
    if request.method == 'GET':
        return Response(CategorySerializer(Category.objects.all(), many=True).data)
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# ─── Lessons ──────────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def lessons_list(request):
    if request.method == 'GET':
        qs = Lesson.objects.filter(is_published=True).select_related('category')
        cat = request.query_params.get('category_id')
        diff = request.query_params.get('difficulty')
        if cat:
            qs = qs.filter(category_id=cat)
        if diff:
            qs = qs.filter(difficulty=diff)
        return Response(LessonSerializer(qs, many=True).data)

    serializer = LessonDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def lesson_detail(request, pk):
    try:
        lesson = Lesson.objects.select_related('category').get(pk=pk, is_published=True)
    except Lesson.DoesNotExist:
        return Response({'detail': 'Не найдено'}, status=404)
    return Response(LessonDetailSerializer(lesson).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_lesson(request, pk):
    try:
        lesson = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        return Response({'detail': 'Не найдено'}, status=404)

    progress, created = UserLessonProgress.objects.get_or_create(
        user=request.user, lesson=lesson
    )
    if progress.is_completed:
        return Response({'message': 'Уже завершён', 'xp_earned': 0, 'coins_earned': 0})

    progress.is_completed = True
    progress.completed_at = timezone.now()
    progress.time_spent_seconds = request.data.get('time_spent_seconds', 0)
    progress.save()

    request.user.lessons_completed += 1
    request.user.save()

    reward = request.user.award(xp=lesson.xp_reward, coins=lesson.coin_reward)
    new_achievements = check_and_grant(request.user)

    return Response({**reward, 'new_achievements': new_achievements})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_lesson_progress(request):
    progress = UserLessonProgress.objects.filter(user=request.user)
    return Response(LessonProgressSerializer(progress, many=True).data)


# ─── Tests ────────────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def tests_list(request):
    if request.method == 'GET':
        qs = Test.objects.filter(is_published=True)
        if request.query_params.get('difficulty'):
            qs = qs.filter(difficulty=request.query_params['difficulty'])
        return Response(TestSerializer(qs, many=True).data)

    # POST — создать тест (с вопросами)
    questions_data = request.data.pop('questions', [])
    serializer = TestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    test = serializer.save()
    for idx, q in enumerate(questions_data):
        Question.objects.create(test=test, order_index=idx, **q)
    return Response(TestSerializer(test).data, status=201)


@api_view(['GET'])
@permission_classes([AllowAny])
def test_detail(request, pk):
    try:
        test = Test.objects.prefetch_related('questions').get(pk=pk, is_published=True)
    except Test.DoesNotExist:
        return Response({'detail': 'Не найдено'}, status=404)
    return Response(TestDetailSerializer(test).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_test(request, pk):
    try:
        test = Test.objects.prefetch_related('questions').get(pk=pk)
    except Test.DoesNotExist:
        return Response({'detail': 'Не найдено'}, status=404)

    answers = request.data.get('answers', {})
    time_spent = request.data.get('time_spent_seconds', 0)

    questions = {str(q.id): q for q in test.questions.all()}
    correct_count = 0
    xp_earned = 0
    coins_earned = 0
    answers_detail = []

    for q_id, chosen in answers.items():
        q = questions.get(q_id)
        if not q:
            continue
        is_correct = chosen == q.correct_answer
        if is_correct:
            correct_count += 1
            xp_earned += q.xp_reward
            coins_earned += q.coin_reward
        answers_detail.append({
            'question_id': int(q_id),
            'question_text': q.text,
            'chosen': chosen,
            'correct_answer': q.correct_answer,
            'is_correct': is_correct,
            'explanation': q.explanation,
        })

    total = test.questions.count()
    score = (correct_count / total * 100) if total > 0 else 0
    passed = score >= test.pass_score

    if passed:
        xp_earned += test.xp_reward
        coins_earned += test.coin_reward

    attempt = TestAttempt.objects.create(
        user=request.user, test=test,
        score=score, correct_count=correct_count,
        total_questions=total, xp_earned=xp_earned,
        coins_earned=coins_earned, passed=passed,
        time_spent_seconds=time_spent, answers=answers,
    )

    request.user.tests_completed += 1
    request.user.save()

    if score == 100:
        check_and_grant_single(request.user, 'perfect_test')

    request.user.award(xp=xp_earned, coins=coins_earned)
    new_achievements = check_and_grant(request.user)

    return Response({
        'attempt_id': attempt.id,
        'score': score,
        'correct_count': correct_count,
        'total_questions': total,
        'passed': passed,
        'xp_earned': xp_earned,
        'coins_earned': coins_earned,
        'answers_detail': answers_detail,
        'new_achievements': new_achievements,
    })


def check_and_grant_single(user, code):
    try:
        achievement = Achievement.objects.get(code=code)
        if not UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            UserAchievement.objects.create(user=user, achievement=achievement)
            if achievement.xp_reward or achievement.coin_reward:
                user.award(xp=achievement.xp_reward, coins=achievement.coin_reward)
    except Achievement.DoesNotExist:
        pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_test_attempts(request):
    attempts = TestAttempt.objects.filter(user=request.user)
    return Response(TestAttemptSerializer(attempts, many=True).data)


# ─── Flashcards ───────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def flashcard_decks(request):
    if request.method == 'GET':
        qs = FlashcardDeck.objects.filter(is_published=True).select_related('category').prefetch_related('cards')
        if request.query_params.get('category_id'):
            qs = qs.filter(category_id=request.query_params['category_id'])
        return Response(FlashcardDeckSerializer(qs, many=True).data)

    cards_data = request.data.pop('cards', [])
    serializer = FlashcardDeckSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    deck = serializer.save()
    for idx, c in enumerate(cards_data):
        Flashcard.objects.create(deck=deck, order_index=idx, **c)
    return Response(FlashcardDeckSerializer(deck).data, status=201)


@api_view(['GET'])
@permission_classes([AllowAny])
def flashcard_deck_detail(request, pk):
    try:
        deck = FlashcardDeck.objects.prefetch_related('cards').select_related('category').get(pk=pk)
    except FlashcardDeck.DoesNotExist:
        return Response({'detail': 'Не найдено'}, status=404)
    return Response(FlashcardDeckDetailSerializer(deck).data)


# ─── Battles ──────────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def battles_list(request):
    if request.method == 'GET':
        battles = Battle.objects.filter(status='waiting').prefetch_related(
            'participants__user'
        )[:20]
        return Response(BattleSerializer(battles, many=True).data)

    battle = Battle.objects.create(
        test_id=request.data.get('test_id')
    )
    BattleParticipant.objects.create(battle=battle, user=request.user)
    battle.refresh_from_db()
    return Response(
        BattleSerializer(Battle.objects.prefetch_related('participants__user').get(pk=battle.pk)).data,
        status=201
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def battle_detail(request, pk):
    try:
        battle = Battle.objects.prefetch_related('participants__user').get(pk=pk)
    except Battle.DoesNotExist:
        return Response({'detail': 'Не найдено'}, status=404)
    return Response(BattleSerializer(battle).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def battle_join(request, pk):
    try:
        battle = Battle.objects.prefetch_related('participants__user').get(pk=pk)
    except Battle.DoesNotExist:
        return Response({'detail': 'Не найдено'}, status=404)

    if battle.status != 'waiting':
        return Response({'detail': 'Батл уже начался или завершён'}, status=400)
    if battle.participants.count() >= 2:
        return Response({'detail': 'Батл заполнен'}, status=400)
    if battle.participants.filter(user=request.user).exists():
        return Response({'detail': 'Уже в батле'}, status=400)

    BattleParticipant.objects.create(battle=battle, user=request.user)
    battle.status = 'in_progress'
    battle.save()

    return Response(BattleSerializer(Battle.objects.prefetch_related('participants__user').get(pk=pk)).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def battle_answer(request, pk):
    try:
        battle = Battle.objects.get(pk=pk)
        participant = BattleParticipant.objects.get(battle=battle, user=request.user)
    except (Battle.DoesNotExist, BattleParticipant.DoesNotExist):
        return Response({'detail': 'Не найдено'}, status=404)

    if battle.status != 'in_progress':
        return Response({'detail': 'Батл не активен'}, status=400)

    q_id = str(request.data.get('question_id'))
    chosen = request.data.get('answer')

    if q_id in participant.answers:
        return Response({'message': 'Уже отвечено', 'correct': False})

    try:
        question = Question.objects.get(pk=int(q_id))
    except Question.DoesNotExist:
        return Response({'detail': 'Вопрос не найден'}, status=404)

    is_correct = chosen == question.correct_answer
    answers = dict(participant.answers)
    answers[q_id] = chosen
    participant.answers = answers
    if is_correct:
        participant.score += 1
    participant.save()

    return Response({'correct': is_correct, 'correct_answer': question.correct_answer})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def battle_finish(request, pk):
    try:
        battle = Battle.objects.prefetch_related('participants__user').get(pk=pk)
    except Battle.DoesNotExist:
        return Response({'detail': 'Не найдено'}, status=404)

    if battle.status == 'finished':
        return Response(BattleSerializer(battle).data)

    battle.status = 'finished'
    battle.finished_at = timezone.now()

    participants = list(battle.participants.all())
    if participants:
        winner_p = max(participants, key=lambda p: p.score)
        battle.winner = winner_p.user
        battle.save()

        from django.conf import settings as s
        for p in participants:
            is_winner = p.user_id == winner_p.user_id
            p.xp_earned = s.RPG_BATTLE_WIN_XP if is_winner else s.RPG_BATTLE_WIN_XP // 2
            p.coins_earned = s.RPG_BATTLE_WIN_COINS if is_winner else s.RPG_BATTLE_WIN_COINS // 2
            p.save()

            user = p.user
            user.battles_played += 1
            if is_winner:
                user.battles_won += 1
            user.save()
            user.award(xp=p.xp_earned, coins=p.coins_earned)
            check_and_grant(user)
    else:
        battle.save()

    return Response(BattleSerializer(Battle.objects.prefetch_related('participants__user').get(pk=pk)).data)
