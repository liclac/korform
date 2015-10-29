from django.views.generic import DetailView
from .models import Group, Sheet

class GroupView(DetailView):
    model = Group
    context_object_name = 'group'
    
    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)
        
        columns = self.get_columns()
        members = self.object.members.all()
        
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
    
    def get_columns(self):
        term = self.request.site.config.current_term
        if term.sheet_id:
            return term.sheet.columns.all()
        elif term.form_id:
            return Sheet.columns_from_form(term.form)
        return Sheet.get_default_columns()
