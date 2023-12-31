# Generated by Django 4.2.3 on 2023-11-21 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchoolManage', '0003_auto_20231118_2253'),
    ]

    operations = [
        migrations.CreateModel(
            name='UICustomization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_snippet', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'Role & Permissions', 'verbose_name_plural': 'Roles & Permissions'},
        ),
        migrations.AlterModelOptions(
            name='rolepermission',
            options={'verbose_name': 'Permission', 'verbose_name_plural': 'Permissions'},
        ),
    ]
