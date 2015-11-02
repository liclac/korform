import datetime
from django import forms
from django.test import TestCase
from django.contrib.sites.models import Site
from korform_accounts.models import Profile
from korform_roster.models import Member
from korform_planning.models import Group, Term, Event, Form, FormField, Sheet, SheetColumn

class TestEvent(TestCase):
    def setUp(self):
        self.site = Site.objects.first()
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

class TestSheet(TestCase):
    def setUp(self):
        self.site = Site.objects.first()
        self.profile = Profile.objects.create()
        self.group = Group.objects.create(site=self.site, name=u"Group", code=u"g", slug=u"g", sort=u"g")
        self.member = Member.objects.create(
            site=self.site, profile=self.profile, group=self.group,
            first_name=u"John", last_name=u"Smith", birthday=datetime.date(2000, 12, 24)
        )
        self.form = Form.objects.create(name=u"Test Form")
    
    def test_default_columns(self):
        cols = Sheet.get_default_columns()
        self.assertEqual(2, len(cols))
        self.assertEqual(u"John Smith", cols[0].render(self.member))
        self.assertEqual(u"2000-12-24", cols[1].render(self.member))
    
    def test_default_columns_included(self):
        cols = Sheet.columns_from_form(self.form)
        self.assertEqual(2, len(cols))
        self.assertEqual(u"John Smith", cols[0].render(self.member))
        self.assertEqual(u"2000-12-24", cols[1].render(self.member))
    
    def test_column_positions(self):
        self.form.fields = [ FormField(label=u"Col 1"), FormField(label=u"Col 2") ]
        cols = Sheet.columns_from_form(self.form)
        self.assertEqual([0, 1, 2, 3], [col.position for col in cols])
    
    def test_column_attributes(self):
        self.form.fields = [ FormField(label=u"Label", key='key') ]
        cols = Sheet.columns_from_form(self.form)
        self.assertEqual(u"Label", cols[2].label)
        self.assertEqual('key', cols[2].key)
    
    def test_column_public_respected(self):
        self.form.fields = [ FormField(label=u"Public"), FormField(label=u"Private", public=False) ]
        cols = Sheet.columns_from_form(self.form)
        self.assertEqual(3, len(cols))
        self.assertEqual(u"Public", cols[2].label)

class TestSheetColumn(TestCase):
    def setUp(self):
        self.site = Site.objects.first()
        self.profile = Profile.objects.create()
        self.group = Group.objects.create(site=self.site, name=u"Group", code=u"g", slug=u"g", sort=u"g")
        self.member = Member.objects.create(
            site=self.site, profile=self.profile, group=self.group,
            first_name=u"John", last_name=u"Smith", birthday=datetime.date(2000, 12, 24),
            extra={ u'key': u'value' }
        )
        self.sheet = Sheet.objects.create(name=u"Test Sheet")
        self.column = SheetColumn.objects.create(sheet=self.sheet, label=u"Label")
    
    def test_render_first_name(self):
        self.column.key = 'first_name'
        self.assertEqual(u"John", self.column.render(self.member))
    
    def test_render_last_name(self):
        self.column.key = 'last_name'
        self.assertEqual(u"Smith", self.column.render(self.member))
    
    def test_render_birthday(self):
        self.column.key = 'birthday'
        self.assertEqual(u"2000-12-24", self.column.render(self.member))
    
    def test_render_group_name(self):
        self.column.key = 'group_name'
        self.assertEqual(u"Group", self.column.render(self.member))
    
    def test_render_group_code(self):
        self.column.key = 'group_code'
        self.assertEqual(u"g", self.column.render(self.member))
    
    def test_render_extra_key(self):
        self.column.key = 'key'
        self.assertEqual(u"value", self.column.render(self.member))
    
    def test_render_invalid_key(self):
        self.column.key = 'invalid_key'
        self.assertEqual(u"", self.column.render(self.member))
    
    def test_render_invalid_key_default(self):
        self.column.key = 'invalid_key'
        self.column.default = u"-"
        self.assertEqual(u"-", self.column.render(self.member))
    
    def test_render_out_of_bounds(self):
        self.column.key = 'first_name'
        self.column.format_string = u"{0} {1}."
        self.assertEqual(u"John .", self.column.render(self.member))
    
    def test_render_space(self):
        self.column.format_string = u" "
        self.assertEqual(u"", self.column.render(self.member))
    
    def test_render_space_default(self):
        self.column.format_string = u" "
        self.column.default = u"-"
        self.assertEqual(u"-", self.column.render(self.member))
    
    def test_render_multiple_keys(self):
        self.column.key = 'first_name,last_name'
        self.assertEqual(u"John Smith", self.column.render(self.member))
    
    def test_render_multiple_keys_with_spaces(self):
        self.column.key = 'first_name, last_name'
        self.assertEqual(u"John Smith", self.column.render(self.member))
    
    def test_render_no_key(self):
        self.column.key = ''
        self.column.format_string = u"{first_name} {last_name}"
        self.assertEqual(u"John Smith", self.column.render(self.member))
