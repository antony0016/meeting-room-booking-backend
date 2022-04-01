from meeting_rooms import models
from meeting_rooms.serializers import ReservationSerializer, MeetingRoomSerializer, LocationSerializer, \
    RoomExchangeRequestSerializer, RoomExchangeRequestRetrieveSerializer

from general.time_process import is_overlap

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from datetime import date, datetime


# todo: 1. implement filter REQUESTING/ACCEPT/REJECT request
# todo: 2. pop a message when exchange request accepted
class RoomExchangeRequestViewSet(ModelViewSet):
    queryset = models.RoomExchangeRequest.objects.filter(read=False, reservation_id__use_date__gte=date.today(),
                                                         is_deleted=False)
    serializer_class = RoomExchangeRequestSerializer

    def get_queryset(self):
        if self.action in ["list", "read"]:
            self.queryset = models.RoomExchangeRequest.objects.filter(read=False,
                                                                      reservation_id__use_date__gte=date.today(),
                                                                      is_deleted=False)
        if self.action in ["partial_update", "update"]:
            return self.queryset.filter(status="REQUESTING")
        # print(requests[0].reservation_id.use_date)
        return self.queryset

    def get_serializer_class(self):
        if self.action in ["list", "read"]:
            return RoomExchangeRequestRetrieveSerializer
        # if self.action in ["partial_update"]:
        #     return RoomExchangeRequestRetrieveSerializer
        return RoomExchangeRequestRetrieveSerializer

    @swagger_auto_schema(
        operation_summary="Create a reservation exchange request.",
        operation_description="Create a reservation exchange request."
    )
    def create(self, request, *args, **kwargs):
        new_exchange_request = self.get_serializer_class()(data=request.data)
        # check new request is valid
        if not new_exchange_request.is_valid():
            return Response({"message": "field wrong"}, status=status.HTTP_400_BAD_REQUEST)
        # get reservation of new exchange
        reservation = new_exchange_request.validated_data.get("reservation_id")
        # check date is greater than today
        if reservation.use_date < date.today():
            return Response({"message": "can't ask a past reservation"}, status=status.HTTP_400_BAD_REQUEST)
        # check the same user can't send request more than one
        requester = new_exchange_request.validated_data.get("requester_id")
        same_request = self.get_queryset().filter(reservation_id=reservation.id, requester_id=requester.id,
                                                  is_deleted=False)
        if len(same_request) > 0:
            return Response({"message": "can't send request more than one!"}, status=status.HTTP_400_BAD_REQUEST)
        new_exchange_request.save()
        return Response({"message": "make exchange request success"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update exchange request status when user reply.",
        operation_description="Update exchange request when user reply."
    )
    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        exchange_requests = self.get_queryset().filter(id=pk)
        # exchange_requests = self.get_serializer_class()(data=request.data)
        # check request is exist
        if len(exchange_requests) != 1:
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        reply = request.data.get("reply")
        exchange_status = request.data.get("status")
        if exchange_status == "ACCEPT":
            reservation = models.Reservation.objects.get(id=exchange_requests[0].reservation_id.id)
            reservation.user_id = exchange_requests[0].requester_id
            reservation.save()
        exchange_requests[0].reply = reply
        exchange_requests[0].status = exchange_status
        exchange_requests[0].save()
        response_data = self.get_serializer_class()(exchange_requests, many=True)
        return Response({"message": "reply success", "data": response_data.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update exchange request read status when user read the reply.",
        operation_description="Update exchange request read status when user read the reply."
    )
    @action(url_path="read", url_name="readRequest", detail=True, methods=["GET"])
    def read_request(self, request, pk=None):
        requests = self.get_queryset().filter(id=pk)
        if len(requests) == 0:
            return Response({"message": "request not found"}, status=status.HTTP_404_NOT_FOUND)
        for request in requests:
            request.read = True
            request.save()
        return Response({"message": "user already read the message"})


class ReservationViewSet(ModelViewSet):
    queryset = models.Reservation.objects.filter(is_deleted=False, room_id__reservation__is_deleted=False).order_by(
        "use_date", "id")
    serializer_class = ReservationSerializer

    def get_queryset(self):
        if self.action in ["retrieve", "list"]:
            self.queryset = models.Reservation.objects.filter(is_deleted=False).order_by("use_date", "id")
        return self.queryset

    def get_serializer_class(self):
        if self.action in []:
            return ReservationSerializer
        return ReservationSerializer

    # todo: date with range
    @swagger_auto_schema(
        operation_summary="Create a new reservation.",
        operation_description="Create a new reservation."
    )
    def create(self, request, *args, **kwargs):
        new_reservation = self.serializer_class(data=request.data)
        if not new_reservation.is_valid(raise_exception=False):
            return Response({"message": "new reservation invalid"}, status=status.HTTP_400_BAD_REQUEST)

        # check the date is greater than now
        reservations_to_compare = self.get_queryset().filter(use_date=request.data.get("use_date"),
                                                             room_id=request.data.get("room_id"), is_deleted=False)
        if new_reservation.validated_data.get("use_date") < date.today():
            return Response({"message": "can't reserve a past date"}, status=status.HTTP_400_BAD_REQUEST)

        # is_today = new_reservation.validated_data.get("use_date") == date.today().isoformat()
        # start_time = new_reservation.validated_data.get("start_time")
        # end_time = new_reservation.validated_data.get("end_time")
        # check date is not overlap
        for post_reservation in reservations_to_compare:
            validated_post_reservation = self.serializer_class(post_reservation)
            if is_overlap(validated_post_reservation.data, new_reservation.validated_data):
                return Response({"message": "date overlapped"}, status=status.HTTP_409_CONFLICT)

        new_reservation.save()

        return Response({"message": "make reservation success", "data": new_reservation.data})

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        reservations = self.get_queryset().filter(id=pk)
        new_reservation = self.serializer_class(data=request.data)
        if len(reservations) != 1:
            return Response({"message": "reservation is not found"}, status=status.HTTP_404_NOT_FOUND)
        if not new_reservation.is_valid():
            return Response({"message": "request is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        # prevent user change past reservation
        time = [str(datetime.now().time().hour), str(datetime.now().time().minute)]
        formatted_time = ["0" if len(t) == 1 else "" + t for t in time]
        now_time = ":".join(formatted_time)
        # print(reservations[0].start_time, reservations[0].end_time, now_time)
        if reservations[0].use_date == date.today().isoformat():
            start_time_lte = reservations[0].start_time <= now_time or new_reservation.validated_data.get(
                "start_time") <= now_time
            end_time_lte = reservations[0].end_time <= now_time or new_reservation.validated_data.get(
                "end_time") <= now_time
            if start_time_lte or end_time_lte:
                return Response({"message": "don't modify past reservation"}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, args, kwargs)

    @swagger_auto_schema(
        operation_summary="Destroy reservation in safety way.",
        operation_description="Destroy reservation in safety way(is_delete == True)."
    )
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        reservations = self.get_queryset().filter(id=pk)
        if len(reservations) == 0:
            return Response({"message": "reservation not found"}, status=status.HTTP_404_NOT_FOUND)
        exchange_requests = models.RoomExchangeRequest.objects.filter(reservation_id=pk)

        # prevent user destroy past reservation
        time = [str(datetime.now().time().hour), str(datetime.now().time().minute)]
        formatted_time = ["0" if len(t) == 1 else "" + t for t in time]
        now_time = ":".join(formatted_time)
        # print(now_time)
        start_time_lte = reservations[0].start_time <= now_time
        end_time_lte = reservations[0].end_time <= now_time
        if start_time_lte or end_time_lte:
            return Response({"message": "don't destroy past reservation"}, status=status.HTTP_403_FORBIDDEN)
        # destroy all of exchange request by enable is_deleted field
        for request in exchange_requests:
            request.is_deleted = True
            request.save()
        reservations[0].is_deleted = True
        reservations[0].save()
        data = self.serializer_class(reservations[0]).data
        return Response({"message": "delete reservation success", 'data': data})


class MeetingRoomViewSet(ModelViewSet):
    queryset = models.MeetingRoom.objects.filter(is_deleted=False, location_id__is_deleted=False)
    serializer_class = MeetingRoomSerializer

    def get_queryset(self):
        return models.MeetingRoom.objects.filter(is_deleted=False, location_id__is_deleted=False)

    # def destroy(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk')
    #     rooms = self.get_queryset().filter(id=pk)
    #     if len(rooms) == 0:
    #         return Response({"message": "room not found"}, status=status.HTTP_404_NOT_FOUND)
    #
    #     # prevent user miss destroy room
    #     rooms[0].is_deleted = True
    #     rooms[0].save()
    #     data = self.serializer_class(rooms[0]).data
    #     return Response({"message": "delete room success", 'data': data})


class LocationViewSet(ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        return models.Location.objects.all()

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return LocationSerializer
        return LocationSerializer

    # def destroy(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk')
    #     locations = self.get_queryset().filter(id=pk)
    #     if len(locations) == 0:
    #         return Response({"message": "location not found"}, status=status.HTTP_404_NOT_FOUND)
    #
    #     # prevent user miss destroy location
    #     locations[0].is_deleted = True
    #     locations[0].save()
    #     data = self.serializer_class(locations[0]).data
    #     return Response({"message": "delete reservation success", 'data': data})
