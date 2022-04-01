from django.contrib import admin
from .models import Reservation, RoomExchangeRequest, MeetingRoom, Location

# Register your models here.
admin.site.register(Reservation)
admin.site.register(RoomExchangeRequest)
admin.site.register(MeetingRoom)
admin.site.register(Location)
# @admin.register(Location)
# class LocationAdmin(admin.ModelAdmin):
#     list_display = ["id", "location"]
