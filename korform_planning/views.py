from django.views.generic import DetailView
from .models import Group

class GroupView(DetailView):
    model = Group
    context_object_name = 'group'
