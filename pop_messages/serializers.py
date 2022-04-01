from rest_framework.serializers import ModelSerializer
from pop_messages.models import PopMessage


class PopMessageSerializer(ModelSerializer):
    class Meta:
        model = PopMessage
        fields = '__all__'
