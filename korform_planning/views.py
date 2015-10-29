from django.views.generic import DetailView
from django.utils.functional import cached_property
from .models import Group

class GroupView(DetailView):
    model = Group
    context_object_name = 'group'
    
    @cached_property
    def sheet(self):
        return self.get_sheet()
    
    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)
        
        members = self.object.members.all()
        columns = self.sheet.columns.all()
        
        context['sheet'] = self.sheet
        context['columns'] = columns
        context['members'] = members
        context['rows'] = [
            {
                'member': member,
                'columns': [
                    {
                        'column': column,
                        'value': column.render(member),
                    } for column in columns
                ]
            } for member in members
        ]
        
        return context
    
    def get_sheet(self):
        return self.request.site.config.current_term.sheet
