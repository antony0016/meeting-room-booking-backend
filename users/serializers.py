from rest_framework.serializers import ModelSerializer
from rest_framework import fields
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRetrieveSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name")


class TokenRetrieveSerializer(ModelSerializer):
    token = fields.CharField(allow_null=True)

    class Meta:
        model = User
        fields = ("id", "name", "token")
