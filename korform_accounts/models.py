import datetime
import random
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.functional import cached_property
from django.contrib.auth.models import AbstractUser

class Profile(models.Model):
    '''
    A Profile exists to link users and their data together.
    
    [Users](/admin/korform_accounts/user/) can only have a single profile each, but a profile can
    be used by multiple users. This allows secure sharing of accounts, between eg. two parents,
    using separate logins to access the same data.
    '''
    
    def __unicode__(self):
      usernames = [u.get_full_name() for u in self.users.all()]
      if len(usernames) == 0:
        return u"Orphaned Profile"
      return u"Profile for {0}".format(u', '.join(usernames))

class User(AbstractUser):
    '''
    A User is a single user in the system.
    
    Note that submitted data is not tied to a user, but to a [profile](/admin/korform_accounts/profile/).
    '''
    
    profile = models.ForeignKey(Profile, related_name='users', on_delete=models.PROTECT, null=True, help_text=u"Multiple users may be associated with a single profile. These users will have access to the same data, but with different logins.")
    
    @cached_property
    def shared_users(self):
        return self.get_shared_users()
    
    @cached_property
    def valid_invite_keys(self):
        return self.get_valid_invite_keys()
    
    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name) if self.first_name else \
            self.email or self.username
    
    def get_shared_users(self):
        return self.profile.users.exclude(id=self.id)
    
    def get_valid_invite_keys(self):
        return self.invite_keys.filter(expires__gt=timezone.now())

def create_user_profile(instance, created, raw, **kwargs):
    if raw:
        return
    
    if not instance.profile_id:
        instance.profile = Profile.objects.create()
        instance.save()

def delete_orphaned_profile(instance, **kwargs):
    if instance.profile.users.count() == 0:
        instance.profile.delete()

models.signals.post_save.connect(create_user_profile, sender=User, dispatch_uid='create_user_profile')
models.signals.post_delete.connect(delete_orphaned_profile, sender=User, dispatch_uid='delete_orphaned_profile')

def default_invite_key_expiry():
    return timezone.now() + datetime.timedelta(days=30)

class InviteKey(models.Model):
    '''
    An invite key allows new users to share an existing user's profile.
    
    They are entered on signup, and a valid key assigns them to the issuing user's profile.
    '''
    
    CHARACTERS = "123456789ABCDEF"
    
    user = models.ForeignKey(User, related_name='invite_keys')
    key = models.CharField(max_length=20, blank=True, unique=True, help_text=u"If this is blank, a new key will be generated.")
    expires = models.DateTimeField(default=default_invite_key_expiry, help_text=u"Default is 30 days from now.")
    
    def expires_in(self):
        return self.expires - timezone.now()
    
    def __unicode__(self):
        return self.key
    
    @classmethod
    def generate_key(cls, groups=4, group_length=4):
        rand = random.SystemRandom()
        return '-'.join([''.join([rand.choice(cls.CHARACTERS) for _ in xrange(group_length)]) for _ in xrange(groups)])

def generate_key_for_invite_key(instance, created, raw, **kwargs):
    if raw:
        return
    
    if not instance.key:
        while True:
            try:
                instance.key = instance.__class__.generate_key()
                instance.save()
                break
            except IntegrityError:
                pass

models.signals.post_save.connect(generate_key_for_invite_key, sender=InviteKey, dispatch_uid='generate_key_for_invite_key')
