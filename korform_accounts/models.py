from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(models.Model):
    pass

class User(AbstractUser):
    profile = models.ForeignKey(Profile, related_name='users', on_delete=models.PROTECT, null=True)

def create_user_profile(instance, created, raw, **kwargs):
    if raw:
        return
    
    if not instance.profile_id:
        instance.profile = Profile.objects.create()
        instance.save()

models.signals.post_save.connect(create_user_profile, sender=User, dispatch_uid='create_user_profile')
