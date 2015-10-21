from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.db import models
from jsonfield import JSONField
from korform_planning.models import Event

class Member(models.Model):
    profile = models.ForeignKey('korform_accounts.Profile', related_name='members')
    group = models.ForeignKey('korform_planning.Group', related_name='members')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    extra = JSONField(default={})
    
    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)
    
    def get_events_missing_rsvp(self):
        return Event.objects.exclude(rsvps__member_id=self.id)
    
    def get_absolute_url(self):
        return reverse('member', kwargs={ 'pk': self.pk })
    
    def __unicode__(self):
        return self.get_full_name()

class RSVP(models.Model):
    CHOICES = (
        (1, _(u"Yes")),
        (0, _(u"No")),
        (2, _(u"Maybe")),
    )
    
    member = models.ForeignKey(Member, related_name='rsvps')
    event = models.ForeignKey('korform_planning.Event', related_name='rsvps')
    answer = models.IntegerField(choices=CHOICES)
    comment = models.TextField(blank=True)
