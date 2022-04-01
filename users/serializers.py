from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Nickname


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class NicknameSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="user_id.id", read_only=True)
    username = serializers.CharField(source="user_id.username", read_only=True)
    is_admin = serializers.BooleanField(source="user_id.is_staff", read_only=True)

    class Meta:
        model = Nickname
        fields = ("id", "username", "nickname", "is_admin")
