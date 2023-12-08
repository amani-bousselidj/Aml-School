# context_processors.py

from .models import GeneralSettings


def custom_logo(request):
    try:
        general_settings = GeneralSettings.objects.first()
        return {'custom_logo': general_settings.get_custom_logo_url()}
    except GeneralSettings.DoesNotExist:
        return {'custom_logo': None}
