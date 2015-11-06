from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import View, DetailView
from django.views.generic.edit import FormView
from registration.backends.default.views import RegistrationView as DefaultRegistrationView
from .forms import RegistrationForm, UserForm
from .models import InviteKey

class RegistrationView(DefaultRegistrationView):
    form_class = RegistrationForm

class SettingsView(FormView):
    form_class = UserForm
    template_name = 'korform_accounts/settings.html'
    success_url = reverse_lazy('account_settings')
    
    def get_form_kwargs(self):
        kwargs = super(SettingsView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        return super(SettingsView, self).form_valid(form)

class CreateInviteKeyView(View):
    def get(self, request):
        key = InviteKey.objects.create(profile=request.user.profile)
        return redirect(reverse('invite', kwargs={'pk': key.pk}))

class DeleteInviteKeyView(View):
    def get(self, request, pk):
        key = get_object_or_404(InviteKey, pk=pk)
        key.delete()
        return redirect(reverse('account_settings'))

class InviteKeyView(DetailView):
    model = InviteKey
    context_object_name = 'key'
    
    def get_queryset(self):
        return super(InviteKeyView, self).get_queryset().filter(profile=self.request.user.profile)
