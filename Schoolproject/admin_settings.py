def get_dynamic_site_logo(context):
    from SchoolManage.models import GeneralSettings  # Import inside the function

    general_settings = GeneralSettings.objects.first()
    if general_settings and general_settings.logo:
        return general_settings.logo.url
    return '/static/admin/img/about-image-02.png'  # Default logo URL
