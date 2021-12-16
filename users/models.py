import hashlib

from django.db import models


class User(models.Model):
    name = models.TextField()
    password = models.TextField()

    def get_token(self):
        token_data = self.name + self.password
        token = hashlib.sha256(token_data.encode("utf-8")).hexdigest()
        return token
