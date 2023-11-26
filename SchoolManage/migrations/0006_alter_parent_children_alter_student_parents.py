# Generated by Django 4.2.3 on 2023-11-25 22:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchoolManage', '0005_alter_student_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='children',
            field=models.ManyToManyField(limit_choices_to={'role__exact': 'student'}, related_name='parents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='parents',
            field=models.ManyToManyField(limit_choices_to={'role__name': 'Parent'}, related_name='children', to=settings.AUTH_USER_MODEL),
        ),
    ]
