from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'password', 'coins', 'xp', 'hearts']
        extra_kwargs = {
            'password': {'write_only': True},
            'coins': {'read_only': True},
            'xp': {'read_only': True},
            'hearts': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Users(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            raise serializers.ValidationError('Неверное имя пользователя или пароль')

        if not user.check_password(password):
            raise serializers.ValidationError('Неверное имя пользователя или пароль')

        refresh = RefreshToken.for_user(user)
        refresh['user_id'] = str(user.id) 

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'email': user.email
        }