from rest_framework.viewsets import ModelViewSet

from meeting_rooms import models, serializers


class ReservationViewSet(ModelViewSet):
    queryset = models.Reservation.objects.all()
    serializer_class = serializers.ReservationSerializer

    def get_serializer_class(self):
        if self.action in []:
            return serializers.ReservationSerializer
        return serializers.ReservationSerializer


class MeetingRoomViewSet(ModelViewSet):
    queryset = models.MeetingRoom.objects.all()
    serializer_class = serializers.MeetingRoomSerializer


class LocationViewSet(ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
