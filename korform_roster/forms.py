from django import forms
from django.utils.translation import ugettext as _
from django.forms.models import modelformset_factory
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from korform_planning.models import FormField
from .models import Member, RSVP

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'birthday')
        widgets = {
            'birthday': forms.DateInput(attrs={'placeholder': _(u"YYYY-MM-dd")})
        }
    
    def __init__(self, form, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        
        self.extra_keys = []
        for field in form.fields.all():
            self.fields[field.key] = field.create_field()
            if field.key in self.instance.extra:
                self.initial[field.key] = self.instance.extra[field.key]
            self.extra_keys.append(field.key)
        
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

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ('answer', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': _(u"Required for \"No\" and \"Maybe\".")})
        }
    
    answer = forms.TypedChoiceField(widget=forms.RadioSelect, choices=RSVP.CHOICES, coerce=int, required=True)

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
