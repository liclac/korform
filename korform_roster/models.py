from django.core.urlresolvers import reverse
from django.db import models
from jsonfield import JSONField

class Member(models.Model):
    profile = models.ForeignKey('korform_accounts.Profile', related_name='members')
    group = models.ForeignKey('korform_planning.Group', related_name='members')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    extra = JSONField(default={})
    
    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)
    
    def get_absolute_url(self):
        return reverse('member', kwargs={ 'pk': self.pk })
    
    def __unicode__(self):
        return self.get_full_name()
