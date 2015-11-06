from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _
from registration.forms import RegistrationFormUniqueEmail
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from .models import User, InviteKey

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
    invite_key = forms.CharField(max_length=20, required=False,
        help_text=u"An existing user can invite you to share their data.",
        widget=forms.TextInput(attrs={'placeholder': u"XXXX-XXXX-XXXX-XXXX"})
    )
    
    class Meta(RegistrationFormUniqueEmail.Meta):
        fields = ('username', 'email', 'first_name', 'last_name')
    
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
            'invite_key',
            FormActions(
                Submit('register', u"Register", css_class='btn-default'),
            ),
        )
    
    def clean_invite_key(self):
        invite_key = self.cleaned_data['invite_key']
        
        if invite_key:
            try:
                InviteKey.objects.get(key=invite_key)
            except InviteKey.DoesNotExist:
                raise forms.ValidationError(_(u"Invalid invite key."), code='invalid')
        
        return invite_key
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        
        if self.cleaned_data['invite_key']:
            key = InviteKey.objects.get(key=self.cleaned_data['invite_key'])
            user.profile = key.profile
            key.delete()
        
        if commit:
            user.save()
        
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.required = True
            field.help_text = u""
                
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            'username',
            'first_name',
            'last_name',
            'email',
            FormActions(
                Submit('save', _(u"Save"), css_class='btn-default'),
            ),
        )
