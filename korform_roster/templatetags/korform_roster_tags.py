from django import template

register = template.Library()

@register.filter
def has_badge(member, request):
    return member.get_badge_count(request) > 0

@register.filter
def badge_count(member, request):
    return member.get_badge_count(request)

@register.filter
def for_site(relation, site):
    return relation.filter(site=site)
