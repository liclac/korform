def badge_counts(request):
    member_badge_count = 0
    for member in request.user.profile.members.all():
        if member.get_badge_count(request):
            member_badge_count += 1
    
    return {
        'member_badge_count': member_badge_count,
    }
