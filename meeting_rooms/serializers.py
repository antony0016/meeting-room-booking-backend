from rest_framework.serializers import ModelSerializer
from rest_framework import fields

from meeting_rooms import models


class LocationSerializer(ModelSerializer):
    class Meta:
        model = models.Location
        fields = '__all__'


class MeetingRoomSerializer(ModelSerializer):
    class Meta:
        model = models.MeetingRoom
        fields = '__all__'


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = '__all__'
