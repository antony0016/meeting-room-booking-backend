from django.db import models

# from users.models import UserWithNickname as User
from django.contrib.auth.models import User

REQUESTING = "REQUESTING"
ACCEPT = "ACCEPT"
REJECT = "REJECT"

status = [
    (REQUESTING, "Requesting"),
    (ACCEPT, "Accept"),
    (REJECT, "Reject"),
]


# Create your models here.
class Location(models.Model):
    location_name = models.TextField()

    is_deleted = models.BooleanField(default=False)


class MeetingRoom(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='rooms')
    room_name = models.TextField()

    is_deleted = models.BooleanField(default=False)


class Reservation(models.Model):
    # fk
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    room_id = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)

    host = models.TextField(default='', blank=True)
    use_date = models.DateField()
    start_time = models.TextField()
    end_time = models.TextField()
    reason = models.TextField()
    attendee = models.IntegerField(default=0)
    guest = models.IntegerField(default=0)
    tea = models.IntegerField(default=0)
    water = models.IntegerField(default=0)
    coffee = models.IntegerField(default=0)
    water_dispenser = models.BooleanField(default=False)
    meal_courtyard = models.IntegerField(default=0)
    meal_buffet = models.IntegerField(default=0)
    note = models.TextField(default='', blank=True)

    created_date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)


class RoomExchangeRequest(models.Model):
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='requests')
    requester_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    replier_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receive_requests")
    status = models.CharField(choices=status, default=REQUESTING, max_length=20)
    reason = models.TextField()
    reply = models.TextField(blank=True)

    read = models.BooleanField(default=0)

    created = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
