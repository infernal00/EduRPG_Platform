with open('backend/core/serializers.py', 'r', encoding='utf-8') as f:
    content = f.read()
old = """class UserStatsSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'username', 'email', 'is_active', 'date_joined', 'stats')

    def get_stats(self, obj):
        return UserStatsSerializer(obj).data"""
new = """class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active', 'date_joined')"""
content = content.replace(old, new)
with open('backend/core/serializers.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
