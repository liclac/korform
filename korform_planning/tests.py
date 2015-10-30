import datetime
from django import forms
from django.test import TestCase
from django.contrib.sites.models import Site
from .models import Term, Event, Form, FormField

class TestEvent(TestCase):
    def setUp(self):
        self.site = Site.objects.create(domain=u"google.com", name=u"Google")
        self.term = Term.objects.create(site=self.site, name=u"Test Term")
        self.event = Event.objects.create(term=self.term, name=u"Test Event")
    
    def test_subtitle_nothing(self):
        '''Subtitle with no additional info should be blank.'''
        self.assertEqual(self.event.get_subtitle(), u"")
    
    def test_subtitle_with_start(self):
        self.event.start = datetime.datetime(2000,12,24,13,37)
        self.assertEqual(self.event.get_subtitle(), u"Dec 24 13:37")
    
    def test_subtitle_with_start_date(self):
        self.event.start = datetime.datetime(2000,12,24)
        self.assertEqual(self.event.get_subtitle(), u"Dec 24")
    
    def test_subtitle_with_start_and_end(self):
        self.event.start = datetime.datetime(2000,12,24,13,37)
        self.event.end = datetime.datetime(2000,12,24,14,47)
        self.assertEqual(self.event.get_subtitle(), u"Dec 24 13:37 - 14:47")
    
    def test_subtitle_with_start_and_end_different_days(self):
        self.event.start = datetime.datetime(2000,12,24,13,37)
        self.event.end = datetime.datetime(2000,12,25,14,47)
        self.assertEqual(self.event.get_subtitle(), u"Dec 24 13:37 - Dec 25 14:47")
    
    def test_subtitle_with_start_and_end_dates(self):
        self.event.start = datetime.datetime(2000,12,24)
        self.event.end = datetime.datetime(2000,12,25)
        self.assertEqual(self.event.get_subtitle(), u"Dec 24 - Dec 25")
    
    def test_subtitle_with_subtitle(self):
        self.event.subtitle = u"Subtitle"
        self.assertEqual(self.event.get_subtitle(), u"Subtitle")
    
    def test_subtitle_with_start_and_subtitle(self):
        self.event.start = datetime.datetime(2000,12,24,13,37)
        self.event.subtitle = u"Subtitle"
        self.assertEqual(self.event.get_subtitle(), u"Dec 24 13:37, Subtitle")

class TestFormField(TestCase):
    def setUp(self):
        self.form = Form(name=u"Test Form")
        self.field = FormField(
            form=self.form, key='key', field='textfield',
            label=u"Label", help_text=u"Help text", placeholder=u"Placeholder",
        )
    
    def test_create_field(self):
        f = self.field.create_field()
        self.assertEqual(f.label, u"Label")
        self.assertEqual(f.help_text, u"Help text")
        self.assertEqual(f.widget.attrs['placeholder'], u"Placeholder")
    
    def test_create_field_respects_required(self):
        self.field.required = True
        f = self.field.create_field()
        self.assertEqual(True, f.required)
        
        self.field.required = False
        f = self.field.create_field()
        self.assertEqual(False, f.required)
    
    def test_create_field_textfield(self):
        self.field.field = 'textfield'
        f = self.field.create_field()
        self.assertIsInstance(f, forms.CharField)
        self.assertIsInstance(f.widget, forms.TextInput)
    
    def test_create_field_textarea(self):
        self.field.field = 'textarea'
        f = self.field.create_field()
        self.assertIsInstance(f, forms.CharField)
        self.assertIsInstance(f.widget, forms.Textarea)
    
    def test_create_field_checkbox(self):
        self.field.field = 'checkbox'
        f = self.field.create_field()
        self.assertIsInstance(f, forms.BooleanField)
        self.assertIsInstance(f.widget, forms.CheckboxInput)
