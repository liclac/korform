from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(models.Model):
    pass

def get_new_profile():
    return Profile.objects.create().id

class User(AbstractUser):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, default=get_new_profile)
