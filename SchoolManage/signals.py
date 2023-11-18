# your_app/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Role, RolePermission

@receiver(post_save, sender=Role)
def extend_permissions(sender, instance, **kwargs):
    if instance.name in ['Student', 'Teacher', 'Parent']:
        # Copy default permissions for Student, Teacher, Parent
        default_permissions = RolePermission.objects.filter(role__name=instance.name)
        for permission in default_permissions:
            # Only create if it doesn't exist
            RolePermission.objects.get_or_create(
                role=instance,
                service_name=permission.service_name,
                can_view=permission.can_view,
                can_add=permission.can_add,
                can_change=permission.can_change,
                can_delete=permission.can_delete
            )
