from django.db import models

CONFIRM = "CONFIRM"
REDIRECT = "REDIRECT"

message_type = [
    (CONFIRM, "Confirm"),
    (REDIRECT, "Redirect"),
]


class PopMessage(models.Model):
    title = models.TextField()
    text = models.TextField()
    # type = models.CharField(choices=message_type, default=CONFIRM, max_length=20)

    # redirect path to event panel
    redirect_url = models.TextField(blank="")

    # the object id, let service can use
    object_id = models.IntegerField(blank="")
