from django import forms
from django.utils.translation import ugettext as _
from django.utils.module_loading import import_string
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'birthday')
    
    def __init__(self, form, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        
        self.extra_keys = []
        for field in form.fields.all():
            cls = import_string(field.field)
            kwargs = {
                'label': field.label,
                'help_text': field.help_text,
                'required': field.required,
            }
            f = cls(**kwargs)
            self.fields[field.key] = f
            self.extra_keys.append(field.key)
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        
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
        return self.instance
