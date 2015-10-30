import datetime
from django.test import TestCase
from django.contrib.sites.models import Site
from .models import Term, Event

class TestEvent(TestCase):
    def setUp(self):
        self.site = Site.objects.create(domain=u"google.com", name=u"Google")
        self.term = Term.objects.create(site=self.site, name=u"Test Term")
        self.event = Event.objects.create(term=self.term, name=u"Test Event")
    
    def test_subtitle_nothing(self):
        '''Subtitle with no additional info should be blank.'''
        self.assertEqual(u"", self.event.get_subtitle())
    
    def test_subtitle_with_start(self):
        self.event.start = datetime.datetime(2000,12,24,13,37)
        self.assertEqual(u"Dec 24 13:37", self.event.get_subtitle())
    
    def test_subtitle_with_start_date(self):
        self.event.start = datetime.datetime(2000,12,24)
        self.assertEqual(u"Dec 24", self.event.get_subtitle())
    
    def test_subtitle_with_start_and_end(self):
        self.event.start = datetime.datetime(2000,12,24,13,37)
        self.event.end = datetime.datetime(2000,12,24,14,47)
        self.assertEqual(u"Dec 24 13:37 - 14:47", self.event.get_subtitle())
    
    def test_subtitle_with_start_and_end_different_days(self):
        self.event.start = datetime.datetime(2000,12,24,13,37)
        self.event.end = datetime.datetime(2000,12,25,14,47)
        self.assertEqual(u"Dec 24 13:37 - Dec 25 14:47", self.event.get_subtitle())
    
    def test_subtitle_with_start_and_end_dates(self):
        self.event.start = datetime.datetime(2000,12,24)
        self.event.end = datetime.datetime(2000,12,25)
        self.assertEqual(u"Dec 24 - Dec 25", self.event.get_subtitle())
    
    def test_subtitle_with_subtitle(self):
        self.event.subtitle = u"Subtitle"
        self.assertEqual(u"Subtitle", self.event.get_subtitle())
    
    def test_subtitle_with_start_and_subtitle(self):
        self.event.start = datetime.datetime(2000,12,24,13,37)
        self.event.subtitle = u"Subtitle"
        self.assertEqual(u"Dec 24 13:37, Subtitle", self.event.get_subtitle())
