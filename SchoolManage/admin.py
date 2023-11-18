from django.utils.translation import gettext as _

from django.contrib import admin
from .models import *
from django import forms
from django.contrib import admin
from .models import Role
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.files.storage import default_storage as storage
from django.contrib.auth import get_user_model  # Import the user model
from django.contrib.auth.models import User, Permission

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'user_country', 'email', 'role', 'telephone', 'gender', 'birthday', 'address', 'marital_status', 'profile_picture_thumbnail')
    list_filter = ('role', 'gender', 'marital_status','country')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'telephone')
   
    def profile_picture_thumbnail(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_picture.url)
        return format_html('<img src="{}" width="30" style="border-radius: 50%;" />', '/static/admin/img/avatar2.svg')
    def user_country(self, obj):
        if obj.country:
            flag_url = obj.country.countrie_flag.url
            flag_html = f'<img src="{flag_url}" width="30" style="border-radius: 15%;" />'
            return format_html(flag_html)
        return "N/A"

    profile_picture_thumbnail.short_description = 'Profile Picture'
class StudentAdmin(admin.ModelAdmin):
    list_display = ('formatted_admission_number', 'student_name', 'class_name', 'birthday', 'gender', 'mobile_phone_number')
    list_filter = ('gender', 'class_name')
    readonly_fields = ('formatted_admission_number',)

    def formatted_admission_number(self, obj):
        return str(obj.admission_number)
    formatted_admission_number.short_description = 'Admission Number'
   
class ParentAdmin(admin.ModelAdmin):
    list_display = ('Parent_name', 'Parent_phone', 'Parent_occupation')
    search_fields = ('Parent_name', 'Parent_phone', 'Parent_occupation')

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('personnel_id', 'user', 'role_teacher', 'designation_faculty', 'department', 'basic_salary', 'type_of_contract', 'work_shift', 'work_location', 'registration_date', 'barcode', 'telephone', 'email', 'gender', 'birthday', 'marital_status', 'address', 'is_active')  # Include 'is_active' in the list_display
    list_filter = ('role_teacher', 'department', 'gender', 'marital_status', 'is_active')  # Include 'is_active' in the list_filter
    search_fields = ('personnel_id', 'user__username', 'user__first_name', 'user__last_name', 'email', 'telephone')

    # Rest of your fields and methods...

class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'assign_teacher', 'course_category', 'visibility')
    list_filter = ('assign_teacher', 'course_category', 'visibility')
    search_fields = ('title', 'assign_teacher__user__username', 'course_category__category_name')

# class CourseSectionAdmin(admin.ModelAdmin):
#     list_display = ('section_title')

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson_type')
    list_filter = ('lesson_type', )

# class QuizAdmin(admin.ModelAdmin):
#     list_display = ('title')


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of empty forms to display
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text')

class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_name', 'exam_title', 'date', 'result')
    list_filter = ('class_name', 'date')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name',)

class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('course', 'syllabus_status')

class LiveMeetingAdmin(admin.ModelAdmin):
    list_display = ('meeting_title', 'meeting_date_time','Organizer')

class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name',)

class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'class_name')


class VediolessonAdmin(admin.ModelAdmin):
    list_display=('title','summary')

class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'topic', 'date', 'time_from', 'time_to', 'class_name', 'subject')
    list_filter = ('date', 'class_name', 'subject')

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'section', 'subject', 'homework_date', 'submission_date')
    list_filter = ('class_name', 'section', 'subject', 'homework_date')

class OnlineExamAdmin(admin.ModelAdmin):
    list_display = ('exam_title', 'exam_from_date', 'exam_to_date', 'auto_result_publish_date', 'time_duration', 'attempt')
    list_filter = ('exam_from_date',)

# class PaymentAdmin(admin.ModelAdmin):
# #     list_display = ('payment_type', 'student', 'date_of_payment', 'payment_mode', 'payment_from', 'reference')
# #     list_filter = ('payment_type', 'date_of_payment')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['student', 'video', 'display_star_rating']

    def display_star_rating(self, obj):
        full_stars = int(obj.rating)  # Number of full stars
        remainder = obj.rating - full_stars  # Fractional part for half stars

        full_star_rating = "★" * full_stars
        half_star_rating = "½" if remainder >= 0.5 else ""  # Display half star if remainder is 0.5 or more

        return full_star_rating + half_star_rating

    display_star_rating.short_description = 'Star Rating'
class VideoLessonInline(admin.TabularInline):
    model = VideoLesson
    extra = 1  # Number of empty forms to display

class CourseSectionInline(admin.TabularInline):
    model = CourseSection
    extra = 1  # Number of empty forms to display
    inlines = [VideoLessonInline]
# Register the admin classes
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = [QuestionInline]  # Add the QuestionInline

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text', 'correct_answer')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'assign_teacher', 'course_category', 'visibility')
    list_filter = ('assign_teacher', 'course_category', 'visibility')
    search_fields = ('title', 'assign_teacher__user__username', 'course_category__category_name')
    inlines = [CourseSectionInline]
class CountriesAdmin(admin.ModelAdmin):
     list_display = ('name', 'countrie_flag_picture','Date_Created')
     def countrie_flag_picture(self, obj):
        if obj.countrie_flag:
            return format_html('<img src="{}" width="50" />', obj.countrie_flag.url)
        return "No Logo"
     
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

# admin.site.register(CustomPermission)



admin.site.register(Countries, CountriesAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseSection)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Quiz,QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(ExamResult, ExamResultAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Syllabus, SyllabusAdmin)
admin.site.register(LiveMeeting, LiveMeetingAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(LessonPlan, LessonPlanAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(OnlineExam, OnlineExamAdmin)
admin.site.register(Payment)
admin.site.register(QuestionChoice)
admin.site.register(SubmitedHomworks)
admin.site.register(ShoppingCart)
admin.site.register(Order)
admin.site.register(VideoLesson,VediolessonAdmin)
from django.contrib import admin
from .models import GeneralSettings
from .forms import GeneralSettingsForm
from django.utils.html import format_html

@admin.register(GeneralSettings)
class GeneralSettingsAdmin(admin.ModelAdmin):
    # List all fields in list_display
    list_display = (
        'display_logo',
        'site_name',
        'phone',
        'email',
        # 'facebook',
        # 'twitter',
        # 'youtube',
        # 'instagram',
        # 'tiktok',
        # 'snapchat',
        # 'linkedin',
        
        # 'google_map_link',
        # 'google_map_iframe',
        'address',
        # 'login_timeout',
        # 'about_small',
        # 'seo_keywords',
        # 'seo_description',
        # 'privacy_policy',
        # 'terms_conditions',
        # 'head_tag',
        # 'footer_tag'
         'work_time',
    )

    # Define a custom method to display the logo image
    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" />', obj.logo.url)
        return "No Logo"

    display_logo.short_description = 'Logo'

    # Disable actions like "delete" to prevent accidental changes
    actions = None

    # Define a custom action for updating settings


    # Disable the "Add" permission for GeneralSettings
    def has_add_permission(self, request):
        return False
@receiver(post_save, sender=GeneralSettings)
def update_site_logo(sender, instance, **kwargs):
    if instance.logo:
        # Update the site logo in Django settings
        settings.SITE_LOGO_URL = storage.url(instance.logo.name)
    else:
        # Use a default logo URL if no logo is set
        settings.SITE_LOGO_URL = '/static/admin/img/about-image-02.png'
from django.contrib import admin
from django.contrib import admin
from .models import Role
from django import forms

# class CustomPermissionInline(admin.TabularInline):
#     model = CustomPermission
#     extra = 1
class RoleAdminForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        custom_name = cleaned_data.get('custom_name')

        if custom_name:
            # If custom_name is provided, use it as the name
            self.instance.name = custom_name

        return cleaned_data

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        custom_name = cleaned_data.get('custom_name')

        if name and custom_name:
            raise forms.ValidationError("You can't provide both a predefined name and a custom name.")

        if not name and not custom_name:
            raise forms.ValidationError("You need to provide either a predefined name or a custom name.")

from django.urls import reverse
from django.utils.html import format_html

# class RoleAdmin(admin.ModelAdmin):
#     list_display = ['display_name', 'update_role', 'view_role', 'delete_role']
#     form = RoleForm

#     def display_name(self, obj):
#         return obj.name or obj.custom_name

#     display_name.short_description = 'Name'

#     def update_role(self, obj):
#         update_url = reverse('admin:SchoolManage_role_change', args=[obj.id])
#         return format_html(
#             '<a href="{}">'
#             '<i class="fas fa-edit" aria-hidden="true" title="Update"></i></a>'.format(update_url)
#         )

#     update_role.short_description = 'Update'

#     def view_role(self, obj):
#         view_url = reverse('admin:SchoolManage_role_changelist') + f'{obj.id}/'
#         return format_html(
#             '<a href="{}">'
#             '<i class="fas fa-eye" style="color:#6610F2" aria-hidden="true" title="View"></i></a>'.format(view_url)
#         )

#     view_role.short_description = 'View'

#     def delete_role(self, obj):
#         delete_url = reverse('admin:SchoolManage_role_delete', args=[obj.id])
#         return format_html(
#             '<a href="{}">'
#             '<i class="fas fa-trash" style="color:red"  aria-hidden="true" title="Delete"></i></a>'.format(delete_url)
#         )

#     delete_role.short_description = 'Delete'
#     inlines = [CustomPermissionInline]

# admin.site.register(Role, RoleAdmin)

# from django.contrib import admin
# from django.contrib.admin import TabularInline
# from .models import Role, CustomPermission

# class CustomPermissionInline(admin.TabularInline):
#     model = CustomPermission
#     extra = 0  # Set the number of empty forms to display

# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('name', 'custom_name')
#     inlines = [CustomPermissionInline]
# from django import forms
# from django.contrib import admin
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
# from django.utils.html import format_html
# from .models import Role, CustomPermission

# class CustomPermissionInline(admin.TabularInline):
#     model = CustomPermission
#     extra = 0

# @admin.register(Role)
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('custom_name', 'name', 'view_permissions')
#     inlines = [CustomPermissionInline]

#     def get_form(self, request, obj=None, **kwargs):
#         self.request = request  # Make the request object available within the class
#         return super().get_form(request, obj, **kwargs)

#     def view_permissions(self, obj):
#         # Fetch all content types for your models
#         content_types = ContentType.objects.exclude(app_label='auth')  # Exclude Django models

#         # Create a dictionary to store permissions for each model
#         permissions_dict = {}

#         # Update permissions based on your logic
#         if self.request.method == 'POST':
#             for content_type in content_types:
#                 model_name = content_type.model

#                 can_view = self.request.POST.get(f'{model_name}_can_view')
#                 can_add = self.request.POST.get(f'{model_name}_can_add')
#                 can_change = self.request.POST.get(f'{model_name}_can_change')
#                 can_delete = self.request.POST.get(f'{model_name}_can_delete')

#                 permissions = []

#                 if can_view:
#                     permissions.append('Can View')
#                 if can_add:
#                     permissions.append('Can Add')
#                 if can_change:
#                     permissions.append('Can Change')
#                 if can_delete:
#                     permissions.append('Can Delete')

#                 permissions_dict[model_name] = permissions

#         # Format permissions for display and editing
#         permissions_table = '<form method="POST">'
#         permissions_table += '<table>'
#         permissions_table += '<tr><th>Model</th><th>Can View</th><th>Can Add</th><th>Can Change</th><th>Can Delete</th></tr>'
#         for model, permissions in permissions_dict.items():
#             permissions_table += f'<tr><td>{model}</td>'
#             for action in ['can_view', 'can_add', 'can_change', 'can_delete']:
#                 is_allowed = action in permissions
#                 permissions_table += f'<td><input type="checkbox" name="{model}_{action}" {"checked" if is_allowed else ""}></td>'
#             permissions_table += '</tr>'
#         permissions_table += '</table>'
#         permissions_table += '<input type="submit" value="Save">'
#         permissions_table += '</form>'

#         return format_html(permissions_table)

#     view_permissions.short_description = 'Permissions'

# # Register the Permission model
# admin.site.register(Permission)
from django import forms
from django.contrib import admin
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from .models import Role, RolePermission
from django.db import transaction

class ServiceNameWidget(admin.widgets.AdminTextInputWidget):
    def render(self, name, value, attrs=None, renderer=None):
        try:
            instance = self.choices.queryset.get(pk=value)
            model_name = instance.model
            return model_name
        except self.choices.queryset.model.DoesNotExist:
            return str(value)

class RolePermissionForm(forms.ModelForm):
    class Meta:
        model = RolePermission
        fields = ['service_name', 'can_view', 'can_add', 'can_change', 'can_delete']

    def __init__(self, *args, **kwargs):
        super(RolePermissionForm, self).__init__(*args, **kwargs)
        self.fields['service_name'].disabled = True  # Disable the service_name field

    def clean(self):
        cleaned_data = super().clean()
        # You can add custom validation logic here if needed
        return cleaned_data

class PermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1
    form = RolePermissionForm

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'permissions_preview', 'create_custom_role_link')
    inlines = [PermissionInline]

    def display_name(self, obj):
        return obj.custom_name or obj.name

    display_name.short_description = 'Role Name'

    def permissions_preview(self, obj):
        permissions = RolePermission.objects.filter(role=obj)
        preview = []
        for permission in permissions:
            service_name = permission.get_service_name()
            actions = []
            if permission.can_view:
                actions.append('View')
            if permission.can_add:
                actions.append('Add')
            if permission.can_change:
                actions.append('Change')
            if permission.can_delete:
                actions.append('Delete')
            preview.append(f"{service_name}: {', '.join(actions)}")
        return ' '.join(preview)

    permissions_preview.short_description = 'Permissions Preview'

    def create_custom_role_link(self, obj):
        url = reverse('admin:custom_role_create', args=[obj.pk])
        link = f'<a href="{url}">Create Custom Role</a>'
        return mark_safe(link)

    create_custom_role_link.short_description = 'Create Custom Role'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'POST' and '_create_custom_role' in request.POST:
            custom_name = request.POST.get('custom_name')
            base_role_name = request.POST.get('base_role_name')
            role = Role.create_custom_role(custom_name, base_role_name)

            # Get service name from RolePermission where custom_name is empty
            # and the name of the role is the same as the selected role for the new custom role
            role_permissions = RolePermission.objects.filter(role__name=base_role_name, role__custom_name='')

            with transaction.atomic():
                if role_permissions.exists():
                    for role_permission in role_permissions:
                        # Clone the permission for the new custom role
                        RolePermission.objects.create(
                            role=role,
                            service_name=role_permission.service_name,
                            can_view=role_permission.can_view,
                            can_add=role_permission.can_add,
                            can_change=role_permission.can_change,
                            can_delete=role_permission.can_delete
                        )
                else:
                    # Create default RolePermission entry if none exist
                    RolePermission.objects.create(role=role, service_name='default_service_name')

            return HttpResponseRedirect(reverse('admin:SchoolManage_role_change', args=[role.id]))

        return super().change_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/create_custom_role/', self.change_view, name='custom_role_create'),
        ]
        return custom_urls + urls
