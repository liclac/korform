from django.db import models

class Member(models.Model):
    profile = models.ForeignKey('korform_accounts.Profile', related_name='members')
    group = models.ForeignKey('korform_planning.Group', related_name='members')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    
    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)
    
    def __unicode__(self):
        return self.get_full_name()
