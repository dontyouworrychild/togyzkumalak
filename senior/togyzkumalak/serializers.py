from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import GameHistory, GameSession, Bot, Queue

# class BotSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bot
#         # fields = ('id', 'name', 'difficulty_level')
#         fields = "__all__"
class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = "__all__"

class GameSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        # fields = ('id', 'user')
        fields = "__all__"


class GameHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameHistory
        # fields = ('id', 'game_session', 'pits', 'kazan', 'tuzdyq')
        fields = "__all__"

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'password2', 'first_name', 'last_name') 
        # fields = "__all__"

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
class ListUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name') 
        # fields = "__all__"