from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.sites.models import Site

class Group(models.Model):
    site = models.ForeignKey(Site, related_name='groups')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)
    
    def get_absolute_url(self):
        return reverse('group', kwargs={'slug': self.slug})
    
    def __unicode__(self):
        return self.code

class Term(models.Model):
    site = models.ForeignKey(Site, related_name='terms')
    name = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, related_name='terms')
    
    def __unicode__(self):
        return self.name

class Event(models.Model):
    class Meta:
        ordering = ['position']
    
    term = models.ForeignKey(Term, related_name='events')
    groups = models.ManyToManyField(Group, related_name='events')
    name = models.CharField(max_length=100)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)
    info = models.TextField(blank=True)
    no_answer = models.BooleanField(default=False)
    position = models.PositiveIntegerField(null=True)
    
    def __unicode__(self):
        group_codes = self.groups.values_list('code', flat=True)
        return u"{0} ({1})".format(self.name, u', '.join(group_codes))
