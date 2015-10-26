def badge_counts(request):
    members_badge = 0
    members = request.user.profile.members.all()
    for member in members:
        if member.get_badge_count(request):
            members_badge += 1
    
    return {
        'members_badge': members_badge,
    }
