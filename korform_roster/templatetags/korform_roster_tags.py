from django import template

register = template.Library()

@register.filter
def has_badge(member, request):
    return member.get_badge_count(request) > 0

@register.filter
def badge_count(member, request):
    return member.get_badge_count(request)
