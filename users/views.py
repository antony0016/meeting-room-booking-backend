from users.models import Nickname
from users.serializers import NicknameSerializer

from rest_framework.viewsets import ModelViewSet


class NicknameViewSet(ModelViewSet):
    queryset = Nickname.objects.all()
    serializer_class = NicknameSerializer

    def get_queryset(self):
        if self.action in ["retrieve", "list"]:
            return Nickname.objects.all()
        return Nickname.objects.all()

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return NicknameSerializer
        return NicknameSerializer
