from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from .models import Member
from .forms import MemberForm

class MemberView(DetailView):
    model = Member
    context_object_name = 'member'

class MemberUpdateView(UpdateView):
    model = Member
    context_object_name = 'member'
    
    def get_form(self, form_class=None):
        f = self.request.site.config.current_term.form
        kwargs = self.get_form_kwargs()
        return MemberForm(f, **kwargs)
