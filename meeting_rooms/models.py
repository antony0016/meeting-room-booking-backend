from django.db import models

from users.models import User


# Create your models here.
class Location(models.Model):
    location_name = models.TextField()


class MeetingRoom(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='rooms')
    room_name = models.TextField()


class Reservation(models.Model):
    # fk
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    room_id = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)

    host = models.TextField(default='')
    use_time = models.TextField()
    use_date = models.DateField()
    reason = models.TextField()
    attendee = models.IntegerField(default=0)
    guest = models.IntegerField(default=0)
    tea = models.IntegerField(default=0)
    water = models.IntegerField(default=0)
    coffee = models.IntegerField(default=0)
    water_dispenser = models.BooleanField(default=False)
    meal_courtyard = models.IntegerField(default=0)
    meal_buffet = models.IntegerField(default=0)
    note = models.TextField(default='')
    created_date = models.DateField(auto_now_add=True)
