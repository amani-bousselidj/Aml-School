from django.apps import AppConfig


class SchoolmanageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SchoolManage'
    
    def ready(self):
        # Import models or perform other initialization here
        from django.contrib.auth.models import AbstractUser, Permission as AuthPermission