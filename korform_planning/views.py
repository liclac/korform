from django.views.generic import DetailView
from .models import Group

class GroupView(DetailView):
    model = Group
    context_object_name = 'group'
    
    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)
        
        sheet = self.get_sheet()
        columns = sheet.columns.all()
        members = self.object.members.all()
        
        context['sheet'] = sheet
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
