import hashlib

from users.models import User
from users.serializers import UserSerializer, UserRetrieveSerializer, TokenRetrieveSerializer

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework import status


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return UserRetrieveSerializer
        return UserSerializer


class VerificationViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin):
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        password = request.data.get("password")
        users = self.queryset.filter(name=name, password=password)
        if len(users) == 0:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        data = TokenRetrieveSerializer(users[0]).data
        data['token'] = users[0].get_token()
        return Response({"data": data})

    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        token = request.META.get('HTTP_Authorization'.upper())
        users = self.queryset.filter(id=user_id)
        # print(token)
        if len(users) == 0:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        if "token " in str(token).lower():
            token = token.split(" ")[1]
            if users[0].get_token() == token:
                return Response({"message": "logout success"})
        return Response({"message": "token authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
