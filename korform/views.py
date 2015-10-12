from django.contrib.flatpages.models import FlatPage
from django.shortcuts import render

def index(request):
    flatpage = FlatPage.objects.filter(url='/').first()
    if flatpage:
        template = flatpage.template_name or u'flatpages/default.html'
        return render(request, template, { 'flatpage': flatpage})
    else:
        return render(request, 'index.html')
