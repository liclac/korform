def site_data(request):
    site_config = request.site.config
    return {
        'all_groups': site_config.current_term.groups.all(),
    }
