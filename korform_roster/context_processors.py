def badge_counts(request):
    members_badge = 0
    members = request.user.profile.members.filter(site=request.site)
    for member in members:
        if member.get_badge_count(request):
            members_badge += 1
    
    contacts_badge = 0
    contacts = request.user.profile.contacts.filter(site=request.site)
    if len(members) != 0 and len(contacts) == 0:
        contacts_badge = u"!"
    
    return {
        'members_badge': members_badge,
        'contacts_badge': contacts_badge,
    }
