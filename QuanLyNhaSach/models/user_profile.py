from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    avatar = models.TextField()
    display_name = models.TextField(default="")
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
