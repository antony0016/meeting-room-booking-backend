import hashlib

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Nickname(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="nickname")
    nickname = models.TextField(max_length=20, default="請更改用戶名")


@receiver(post_save, sender=User)
def create_nickname(sender, instance, created, **kwargs):
    # if created:
    Nickname.objects.get_or_create(user_id=instance)
