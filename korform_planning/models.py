from django.db import models
from django.contrib.sites.models import Site

class Term(models.Model):
    site = models.ForeignKey(Site, related_name='terms')
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class Event(models.Model):
    class Meta:
        ordering = ['position']
    
    term = models.ForeignKey(Term, related_name='events')
    name = models.CharField(max_length=100)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)
    info = models.TextField(blank=True)
    no_answer = models.BooleanField(default=False)
    position = models.PositiveIntegerField(null=True)
    
    def __unicode__(self):
        return self.name
