from django import forms
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationFormUniqueEmail
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Field('username', autofocus=True),
            'password',
            FormActions(
                Submit('register', u"Register", css_class='btn-default'),
            ),
        )

class RegistrationForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Field('first_name', autofocus=True),
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            FormActions(
                Submit('register', u"Register", css_class='btn-default'),
            ),
        )
