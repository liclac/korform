from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(models.Model):
    def __unicode__(self):
      usernames = [u.get_full_name() for u in self.users.all()]
      return u"Profile for {0}".format(u', '.join(usernames))

class User(AbstractUser):
    profile = models.ForeignKey(Profile, related_name='users', on_delete=models.PROTECT, null=True)
    
    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name) if self.first_name else \
            self.email
    
    def get_shared_users(self):
        return self.profile.users.exclude(id=self.id)

def create_user_profile(instance, created, raw, **kwargs):
    if raw:
        return
    
    if not instance.profile_id:
        instance.profile = Profile.objects.create()
        instance.save()

models.signals.post_save.connect(create_user_profile, sender=User, dispatch_uid='create_user_profile')
