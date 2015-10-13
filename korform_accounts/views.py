from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from registration.backends.default.views import RegistrationView as DefaultRegistrationView
from .forms import RegistrationForm, SettingsForm

class RegistrationView(DefaultRegistrationView):
    form_class = RegistrationForm

class SettingsView(FormView):
    form_class = SettingsForm
    template_name = 'accounts/settings.html'
    success_url = reverse_lazy('account_settings')
    
    def get_initial(self):
        initial = super(SettingsView, self).get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial
    
    def form_valid(self, form):
        form.save(self.request.user)
        return super(SettingsView, self).form_valid(form)
