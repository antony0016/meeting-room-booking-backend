from rest_framework.viewsets import ModelViewSet

from pop_messages.models import PopMessage
from pop_messages.serializers import PopMessageSerializer


class PopMessageViewSet(ModelViewSet):
    queryset = PopMessage.objects.all()
    serializer_class = PopMessageSerializer
