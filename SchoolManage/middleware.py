from django.contrib.auth import logout
from django.utils import timezone
from datetime import timedelta
from .models import GeneralSettings  # Import your GeneralSettings model

class AdminLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.user.is_staff:
            # Check if GeneralSettings exists and has a valid work_time value
            general_settings = GeneralSettings.objects.first()
            if general_settings and general_settings.work_time:
                work_time = general_settings.work_time

                # Calculate the inactivity time threshold in minutes
                threshold_time = timezone.now() - timedelta(minutes=work_time)

                # If the user's last activity is older than the threshold, log them out
                if request.user.last_login < threshold_time:
                    logout(request)

        return response
