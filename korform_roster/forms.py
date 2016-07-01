from django import forms
from django.utils.translation import ugettext as _
from django.forms.models import modelformset_factory
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from korform_planning.models import FormField
from .models import Member, Contact, RSVP

class CustomizableMixin(object):
    def add_custom_fields(self, form):
        self.extra_keys = []
        
        if not form:
            return
        
        for field in form.fields.all():
            self.fields[field.key] = field.create_field()
            if field.key in self.instance.extra:
                self.initial[field.key] = self.instance.extra[field.key]
            self.extra_keys.append(field.key)

class MemberForm(CustomizableMixin, forms.ModelForm):
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'birthday')
        widgets = {
            'birthday': forms.DateInput(attrs={'placeholder': _(u"YYYY-MM-dd")})
        }
    
    def __init__(self, form, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.add_custom_fields(form)
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        
        layout_fields = [
            Field('first_name', autofocus=True),
            'last_name',
            'birthday',
        ] + self.extra_keys + [
            FormActions(
                Submit('save', _(u"Save"), css_class='btn-default'),
            ),
        ]
        self.helper.layout = Layout(*layout_fields)
    
    def save(self, commit=True):
        super(MemberForm, self).save(commit=False)
        for key in self.extra_keys:
            self.instance.extra[key] = self.cleaned_data[key]
        if commit:
            self.instance.save()
        return self.instance

class ContactForm(CustomizableMixin, forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name')
    
    def __init__(self, form, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.add_custom_fields(form)
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        
        layout_fields = [
            Field('first_name', autofocus=True),
            'last_name',
        ] + self.extra_keys + [
            FormActions(
                Submit('save', _(u"Save"), css_class='btn-default'),
            ),
        ]
        self.helper.layout = Layout(*layout_fields)
    
    def save(self, commit=True):
        super(ContactForm, self).save(commit=False)
        for key in self.extra_keys:
            self.instance.extra[key] = self.cleaned_data[key]
        if commit:
            self.instance.save()
        return self.instance

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ('answer', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2})
        }
    
    answer = forms.TypedChoiceField(widget=forms.RadioSelect, choices=RSVP.CHOICES, coerce=int, required=True)
    
    def make_no_answer(self):
        self.fields['answer'].choices = [(1, "")]
        self.fields['answer'].widget = forms.HiddenInput(attrs={'value': 1})
        self.fields['comment'].widget = forms.HiddenInput()

class RSVPFormSet(forms.BaseModelFormSet):
    def __init__(self, member, events, *args, **kwargs):
        self.member = member
        self.events = events
        self.min_num = len(events)
        self.max_num = len(events)
        super(RSVPFormSet, self).__init__(*args, **kwargs)
    
    def _construct_form(self, i, **kwargs):
        form = super(RSVPFormSet, self)._construct_form(i, **kwargs)
        form.instance.member = self.member
        form.instance.event = self.events[i]
        
        if form.instance.event.no_answer:
            form.make_no_answer()
        
        return form

class RSVPFormSetHelper(FormHelper):
    template = 'korform_roster/forms/rsvp_formset.html'
    
    def __init__(self, *args, **kwargs):
        super(RSVPFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            InlineRadios('answer'),
            'comment'
        )
        self.add_input(Submit('save', _(u"Save")))
