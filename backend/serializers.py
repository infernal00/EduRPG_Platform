from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Category, Lesson, UserLessonProgress, Test, Question,
    TestAttempt, FlashcardDeck, Flashcard, Battle, BattleParticipant,
    Achievement, UserAchievement
)

User = get_user_model()


# ─── Auth ─────────────────────────────────────────────────────────────────────

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email уже используется")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.xp_to_next_level = user.xp_to_reach_level(1)
        user.save()
        return user


# ─── User ─────────────────────────────────────────────────────────────────────

class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'level', 'xp', 'xp_to_next_level', 'coins', 'total_xp_earned',
            'lessons_completed', 'tests_completed', 'battles_won',
            'battles_played', 'streak_days',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar_url', 'is_active', 'date_joined', 'stats')

    def get_stats(self, obj):
        return UserStatsSerializer(obj).data


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar_url', 'level', 'xp')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'avatar_url')


# ─── Category ─────────────────────────────────────────────────────────────────

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'icon', 'color')


# ─── Lesson ───────────────────────────────────────────────────────────────────

class LessonSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )

    class Meta:
        model = Lesson
        fields = (
            'id', 'title', 'slug', 'description', 'difficulty',
            'xp_reward', 'coin_reward', 'order_index', 'is_published',
            'category', 'category_id', 'created_at',
        )


class LessonDetailSerializer(LessonSerializer):
    class Meta(LessonSerializer.Meta):
        fields = LessonSerializer.Meta.fields + ('content',)


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLessonProgress
        fields = ('lesson_id', 'is_completed', 'completed_at', 'time_spent_seconds')


# ─── Test ─────────────────────────────────────────────────────────────────────

class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'text', 'options', 'order_index')

    def get_options(self, obj):
        opts = {'a': obj.option_a, 'b': obj.option_b}
        if obj.option_c:
            opts['c'] = obj.option_c
        if obj.option_d:
            opts['d'] = obj.option_d
        return opts


class QuestionWithAnswerSerializer(QuestionSerializer):
    class Meta(QuestionSerializer.Meta):
        fields = QuestionSerializer.Meta.fields + ('correct_answer', 'explanation', 'xp_reward', 'coin_reward')


class TestSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = (
            'id', 'title', 'description', 'difficulty',
            'time_limit_seconds', 'pass_score', 'xp_reward',
            'coin_reward', 'question_count',
        )

    def get_question_count(self, obj):
        return obj.questions.count()


class TestDetailSerializer(TestSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta(TestSerializer.Meta):
        fields = TestSerializer.Meta.fields + ('questions',)


class TestAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAttempt
        fields = (
            'id', 'test_id', 'score', 'correct_count', 'total_questions',
            'passed', 'xp_earned', 'coins_earned', 'created_at',
        )


# ─── Flashcards ───────────────────────────────────────────────────────────────

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ('id', 'card_type', 'front', 'back', 'hint', 'order_index')


class FlashcardDeckSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    card_count = serializers.SerializerMethodField()

    class Meta:
        model = FlashcardDeck
        fields = ('id', 'title', 'description', 'category', 'card_count')

    def get_card_count(self, obj):
        return obj.cards.count()


class FlashcardDeckDetailSerializer(FlashcardDeckSerializer):
    cards = FlashcardSerializer(many=True, read_only=True)

    class Meta(FlashcardDeckSerializer.Meta):
        fields = FlashcardDeckSerializer.Meta.fields + ('cards',)


# ─── Battle ───────────────────────────────────────────────────────────────────

class BattleParticipantSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = BattleParticipant
        fields = ('user', 'score', 'is_ready', 'xp_earned', 'coins_earned')


class BattleSerializer(serializers.ModelSerializer):
    participants = BattleParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Battle
        fields = ('id', 'status', 'test_id', 'winner_id', 'created_at', 'finished_at', 'participants')


# ─── Achievements ─────────────────────────────────────────────────────────────

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'code', 'title', 'description', 'icon', 'xp_reward', 'coin_reward')


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ('achievement', 'earned_at')


# ─── Leaderboard ──────────────────────────────────────────────────────────────

class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar_url', 'level', 'total_xp_earned', 'battles_won')
