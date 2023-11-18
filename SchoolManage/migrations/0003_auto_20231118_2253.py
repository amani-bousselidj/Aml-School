from django.db import migrations
from SchoolManage.models import Role, RolePermission
from django.contrib.contenttypes.models import ContentType

def populate_default_permissions(apps, schema_editor):
    # Get or create Role objects for Student, Teacher, Parent
    student_role, created = Role.objects.get_or_create(name='Student')
    teacher_role, created = Role.objects.get_or_create(name='Teacher')
    parent_role, created = Role.objects.get_or_create(name='Parent')

    # Define default permissions (service_name, can_view, can_add, can_change, can_delete)
    default_permissions = [
        ('certificate', True, False, False, False),
        ('examresult', True, False, False, False),
        ('lessonplan', True, False, False, False),
        ('payment', True, True, False, False),
        ('livemeeting', True, False, False, False),
        ('rating', True, True, True, True),
        ('shoppingcart', True, True, True, True),
        ('studentanswer', True, False, False, False),
        ('studentattempt', True, True, False, False),
        ('studentprogress', True, False, False, False),
        ('order', True, True, True, True),
        ('teacher', True, False, False, False),
        ('SubmitedHomworks', True, True, True, True),
        ('videolesson', True, False, False, False),
        ('lesson', True, False, False, False),
        ('course', True, False, False, False),
        ('homework', True, False, False, False),
        ('subject', True, False, False, False),
        # Add more permissions as needed
    ]

    # Populate RolePermission entries for Student role
    for service_name, can_view, can_add, can_change, can_delete in default_permissions:
        content_type = ContentType.objects.get_for_model(apps.get_model('SchoolManage', service_name))
        RolePermission.objects.get_or_create(role=student_role, service_name=content_type, can_view=can_view, can_add=can_add, can_change=can_change, can_delete=can_delete)

    # Define default permissions for Teacher role
    teacher_permissions = [
        ('teacher', True, False, False, False),
        ('certificate', True, True, False, False),
        ('examresult', True, True, True, True),
        ('lessonplan', True, True, True, True),
        ('livemeeting', True, True, True, True),
        ('onlineexam', True, True, True, True),
        ('rating', True, True, True, True),
        ('section', True, False, False, False),
        ('studentanswer', True, False, False, False),
        ('studentattempt', True, False, False, False),
        ('studentprogress', True, False, False, False),
        ('SubmitedHomworks', True, False, False, False),
        ('syllabus', True, False, False, False),
        ('videolesson', True, True, True, True),
        ('subject', True, False, False, False),
        ('student', True, False, False, False),
        ('quiz', True, True, True, True),
        ('question', True, True, True, True),
        ('lesson', True, True, True, True),
        ('homework', True, True, True, True),
        ('coursesection', True, True, True, True),
        ('coursecategory', True, True, True, True),
        ('class', True, False, False, False),
        ('course', True, True, True, True),
    ]

    # Populate RolePermission entries for Teacher role
    for service_name, can_view, can_add, can_change, can_delete in teacher_permissions:
        content_type = ContentType.objects.get_for_model(apps.get_model('SchoolManage', service_name))
        RolePermission.objects.get_or_create(role=teacher_role, service_name=content_type, can_view=can_view, can_add=can_add, can_change=can_change, can_delete=can_delete)

    # Define default permissions for Parent role
    parent_permissions = [
        ('certificate', True, False, False, False),
        ('examresult', True, False, False, False),
        ('lessonplan', True, False, False, False),
        ('payment', True, False, False, False),
        ('livemeeting', True, False, False, False),
        ('rating', True, False, False, False),
        ('shoppingcart', True, False, False, False),
        ('studentanswer', True, False, False, False),
        ('studentattempt', True, False, False, False),
        ('studentprogress', True, False, False, False),
        ('order', True, False, False, False),
        ('teacher', True, False, False, False),
        ('SubmitedHomworks', True, False, False, False),
        ('videolesson', True, False, False, False),
        ('lesson', True, False, False, False),
        ('course', True, False, False, False),
        ('homework', True, False, False, False),
        ('subject', True, False, False, False),
        # Add more permissions as needed
    ]

    # Populate RolePermission entries for Parent role
    for service_name, can_view, can_add, can_change, can_delete in parent_permissions:
        content_type = ContentType.objects.get_for_model(apps.get_model('SchoolManage', service_name))
        RolePermission.objects.get_or_create(role=parent_role, service_name=content_type, can_view=can_view, can_add=can_add, can_change=can_change, can_delete=can_delete)

class Migration(migrations.Migration):

    dependencies = [
        ('SchoolManage', '0002_alter_rolepermission_unique_together_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_default_permissions),
    ]
