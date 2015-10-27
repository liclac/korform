from django.contrib.flatpages.models import FlatPage
from django.shortcuts import render

def index(request):
    try:
        flatpage = FlatPage.objects.filter(url='/').get()
        template = flatpage.template_name or u'flatpages/default.html'
        return render(request, template, { 'flatpage': flatpage})
    except FlatPage.DoesNotExist:
        return render(request, 'index.html')
