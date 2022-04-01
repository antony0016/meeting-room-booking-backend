from rest_framework.serializers import ModelSerializer, CharField, IntegerField
from meeting_rooms import models


class LocationSerializer(ModelSerializer):
    class Meta:
        model = models.Location
        fields = '__all__'  # show me


class MeetingRoomSerializer(ModelSerializer):
    class Meta:
        model = models.MeetingRoom
        fields = '__all__'


class ReservationSerializer(ModelSerializer):
    room_name = CharField(source="room_id.room_name", read_only=True)
    nickname = CharField(source="user_id.nickname.nickname", read_only=True)

    class Meta:
        model = models.Reservation
        fields = '__all__'


class RoomExchangeRequestSerializer(ModelSerializer):
    class Meta:
        model = models.RoomExchangeRequest
        fields = '__all__'


class RoomExchangeRequestRetrieveSerializer(ModelSerializer):
    requester_name = CharField(source="requester_id.nickname.nickname", read_only=True)
    replier_name = CharField(source="replier_id.nickname.nickname", read_only=True)
    room_name = CharField(source="reservation_id.room_id.room_name", read_only=True)
    reservation_date = CharField(source="reservation_id.use_date", read_only=True)
    reservation_start_time = CharField(source="reservation_id.start_time", read_only=True)
    reservation_end_time = CharField(source="reservation_id.end_time", read_only=True)

    class Meta:
        model = models.RoomExchangeRequest
        fields = '__all__'

# class RoomExchangeRequestPartialUpdateSerializer(ModelSerializer):
#
#     class Meta:
#         model = models.RoomExchangeRequest
#         fields = '__all__'
