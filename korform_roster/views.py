from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from korform_planning.models import Group
from .models import Member
from .forms import MemberForm

class CustomFormMixin(object):
    def get_form(self, form_class=None):
        f = self.request.site.config.current_term.form
        kwargs = self.get_form_kwargs()
        return MemberForm(f, **kwargs)



class MemberView(DetailView):
    model = Member
    context_object_name = 'member'

class MemberPickGroupView(TemplateView):
    template_name = 'korform_roster/member_group.html'
    
    def get_context_data(self, **kwargs):
        context = super(MemberPickGroupView, self).get_context_data(**kwargs)
        context['groups'] = self.request.site.config.current_term.groups.all()
        return context

class MemberCreateView(CustomFormMixin, CreateView):
    model = Member
    context_object_name = 'member'
    
    def get_group(self):
        return get_object_or_404(Group, slug=self.kwargs['group'])
    
    def get_context_data(self, **kwargs):
        context = super(MemberCreateView, self).get_context_data(**kwargs)
        context['group'] = self.get_group()
        return context
    
    def form_valid(self, form):
        form.instance.group = self.get_group()
        form.instance.profile = self.request.user.profile
        return super(MemberCreateView, self).form_valid(form)

class MemberUpdateView(CustomFormMixin, UpdateView):
    model = Member
    context_object_name = 'member'
