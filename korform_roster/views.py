from django.views.generic import DetailView
from .models import Member

class MemberView(DetailView):
    model = Member
    context_object_name = 'member'
