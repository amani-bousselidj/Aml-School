from django.urls import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from .models import GeneralSettings
from django.contrib import admin
from .models import *
from django import forms
from django.contrib import admin
# from django.contrib.auth.models import User
from django.utils.html import format_html
from django.forms.widgets import Widget


# from admin_tools_stats.models import *


class WebPImageWidget(Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            return format_html('<img src="{}" width="50" />', value.url)
        return "No Image"


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'user_country', 'email', 'role',
                    'telephone', 'gender', 'birthday', 'address', 'marital_status', 'profile_picture_thumbnail')
    list_filter = ('role', 'gender', 'marital_status', 'country')
    search_fields = ('username', 'first_name',
                     'last_name', 'email', 'telephone')

    def profile_picture_thumbnail(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                               obj.profile_picture.url)
        return format_html('<img src="{}" width="30" style="border-radius: 50%;" />', '/static/admin/img/avatar2.svg')

    def user_country(self, obj):
        if obj.country:
            flag_url = obj.country.countrie_flag.url
            flag_html = f'<img src="{flag_url}" width="30" style="border-radius: 15%;" />'
            return format_html(flag_html)
        return "N/A"

    profile_picture_thumbnail.short_description = 'Profile Picture'


class StudentAdmin(admin.ModelAdmin):
    list_display = ('formatted_admission_number', 'username', 'class_name',
                    'birthday', 'gender', 'mobile_phone_number', 'profile_picture_thumbnail')
    list_filter = ('gender', 'class_name')
    readonly_fields = ('formatted_admission_number',)

    def formatted_admission_number(self, obj):
        return str(obj.admission_number)

    def profile_picture_thumbnail(self, obj):
        if obj.user.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                               obj.user.profile_picture.url)
        return format_html('<img src="{}" width="30" style="border-radius: 50%;" />', '/static/admin/img/avatar2.svg')

    def username(self, obj):
        return obj.user.username

    formatted_admission_number.short_description = 'Admission Number'
    profile_picture_thumbnail.short_description = 'Profile Picture'
    username.short_description = 'Username'

    change_list_template = 'admin/change_list_graph.html'


class ParentAdmin(admin.ModelAdmin):
    list_display = ('Parent_name', 'Parent_phone', 'Parent_occupation')
    search_fields = ('Parent_name', 'Parent_phone', 'Parent_occupation')


class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'personnel_id', 'user', 'role_teacher', 'designation_faculty', 'department', 'basic_salary', 'type_of_contract',
        'work_shift', 'work_location',
        # Include 'is_active' in the list_display
        'registration_date', 'barcode', 'telephone', 'email', 'gender', 'birthday', 'marital_status', 'address',
        'is_active')
    # Include 'is_active' in the list_filter
    list_filter = ('role_teacher', 'department', 'gender',
                   'marital_status', 'is_active')
    search_fields = ('personnel_id', 'user__username',
                     'user__first_name', 'user__last_name', 'email', 'telephone')

    # Rest of your fields and methods...


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'assign_teacher', 'course_category', 'visibility')
    list_filter = ('assign_teacher', 'course_category', 'visibility')
    search_fields = ('title', 'assign_teacher__user__username',
                     'course_category__category_name')


# class CourseSectionAdmin(admin.ModelAdmin):
#     list_display = ('section_title')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson_type')
    list_filter = ('lesson_type',)


# class QuizAdmin(admin.ModelAdmin):
#     list_display = ('title')


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of empty forms to display


# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ('question', 'choice_text')

class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_name', 'exam_title', 'date', 'result')
    list_filter = ('class_name', 'date')


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name',)


class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('course', 'syllabus_status')


class LiveMeetingAdmin(admin.ModelAdmin):
    list_display = ('meeting_title', 'meeting_date_time', 'Organizer')


class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name',)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'class_name')


class VediolessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary')


class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'topic', 'date', 'time_from',
                    'time_to', 'class_name', 'subject')
    list_filter = ('date', 'class_name', 'subject')


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'section', 'subject',
                    'homework_date', 'submission_date')
    list_filter = ('class_name', 'section', 'subject', 'homework_date')


class OnlineExamAdmin(admin.ModelAdmin):
    list_display = ('exam_title', 'exam_from_date', 'exam_to_date',
                    'auto_result_publish_date', 'time_duration', 'attempt')
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
        # Display half star if remainder is 0.5 or more
        half_star_rating = "½" if remainder >= 0.5 else ""

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
    search_fields = ('title', 'assign_teacher__user__username',
                     'course_category__category_name')
    inlines = [CourseSectionInline]


class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'countrie_flag_picture', 'Date_Created')

    def countrie_flag_picture(self, obj):
        if obj.countrie_flag:
            return format_html('<img src="{}" width="50" />', obj.countrie_flag.url)
        return "No Logo"


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
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice, ChoiceAdmin)
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
admin.site.register(VideoLesson, VediolessonAdmin)


# admin.py


@admin.register(GeneralSettings)
class GeneralSettingsAdmin(admin.ModelAdmin):
    # List all fields in list_display
    list_display = (
        'display_logo',
        'site_name',
        'phone',
        'email',
        'address',
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


# ...

# @receiver(post_save, sender=GeneralSettings)
# def update_site_logo(sender, instance, **kwargs):
#     print("Signal triggered!")
#     if 'JAZZMIN_SETTINGS' in dir(settings) and 'SITE_LOGO_URL' in settings.JAZZMIN_SETTINGS:
#         if instance.logo:
#             # Update the site logo in Django settings
#             settings.JAZZMIN_SETTINGS['SITE_LOGO_URL'] = instance.logo.url
#         else:
#             # Use a default logo URL if no logo is set
#             settings.JAZZMIN_SETTINGS['SITE_LOGO_URL'] = '/static/admin/img/about-image-02.png'


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
            raise forms.ValidationError(
                "You can't provide both a predefined name and a custom name.")

        if not name and not custom_name:
            raise forms.ValidationError(
                "You need to provide either a predefined name or a custom name.")


# # Register the Permission model
# admin.site.register(Permission)


class ModelNameWidget(forms.Select):
    def label_from_instance(self, obj):
        return obj.model.split('.')[-1]


class RolePermissionForm(forms.ModelForm):
    class Meta:
        model = RolePermission
        fields = ['service_name', 'can_view',
                  'can_add', 'can_change', 'can_delete']

    def __init__(self, *args, **kwargs):
        super(RolePermissionForm, self).__init__(*args, **kwargs)

        # Disable checkboxes based on the principle role's permissions
        # role_instance = getattr(self.instance, 'role', None)
        # principle_role_permissions = role_instance.rolepermission_set.first() if role_instance else None
        # if principle_role_permissions:
        #     self.fields['can_view'].disabled = not principle_role_permissions.can_view
        #     self.fields['can_add'].disabled = not principle_role_permissions.can_add
        #     self.fields['can_change'].disabled = not principle_role_permissions.can_change
        #     self.fields['can_delete'].disabled = not principle_role_permissions.can_delete

        # Disable the service_name field
        self.fields['service_name'].disabled = True


class PermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1
    form = RolePermissionForm

    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name == 'can_delete':
    #         # Set can_delete to True by default in inline form
    #         kwargs['initial'] = True
    #     return super().formfield_for_dbfield(db_field, **kwargs)


# @admin.register(Role)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'create_custom_role_link')
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
        url = reverse('admin:SchoolManage_role_change', args=[obj.pk])
        link = format_html(
            '<a href="{}#role-permissions-tab"><i class="fas fa-edit"></i></a>', url)
        return link

    create_custom_role_link.short_description = 'Create Custom Role'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'POST' and '_create_custom_role' in request.POST:
            custom_name = request.POST.get('custom_name')
            base_role_name = request.POST.get('base_role_name')
            role = Role.create_custom_role(custom_name, base_role_name)

            # Get service name from RolePermission where custom_name is empty
            # and the name of the role is the same as the selected role for the new custom role
            role_permissions = RolePermission.objects.filter(
                role__name=base_role_name, role__custom_name='')

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
                    RolePermission.objects.create(
                        role=role, service_name='default_service_name')

            return HttpResponseRedirect(reverse('admin:SchoolManage_role_change', args=[role.id]))

        return super().change_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/create_custom_role/',
                 self.change_view, name='custom_role_create'),
        ]
        return custom_urls + urls

    def get_queryset(self, request):
        # Filter roles with a non-empty custom name from the list view
        return super().get_queryset(request).exclude(custom_name='').filter(custom_name__isnull=False)


# @admin.register(RolePermission)


class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'display_service_name', 'can_view',
                    'can_add', 'can_change', 'can_delete')

    def display_service_name(self, obj):
        return obj.service_name.model_class().__name__

    display_service_name.short_description = 'Service Name'

    def has_add_permission(self, request):
        return False  # Disable "Add" permission

    def has_change_permission(self, request, obj=None):
        return False  # Disable "Change" permission

    def has_delete_permission(self, request, obj=None):
        return True  # Disable "Delete" permission

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions


class CustomModelAdmin(admin.ModelAdmin):
    # Your customizations for the model admin go here
    pass


# Custom admin site
# from admin_tools_stats.models import *


class CustomAdminSite(admin.AdminSite):
    site_header = 'Adminstration'
    site_title = 'Aml-School'
    index_title = 'Adminstration'

    def index(self, request, extra_context=None):
        app_list = self.get_app_list(request)

        # Exclude the app(s) you want to hide from the dashboard
        excluded_apps = ['SchoolManage']

        # Filter out the excluded apps
        app_list = [app for app in app_list if app['app_label']
                    not in excluded_apps]

        context = {
            'app_list': app_list,
            # 'custom_variable': 'Hello, this is a custom variable!',
        }
        context.update(extra_context or {})

        return super().index(request, context)


# Register your custom admin site
custom_admin_site = CustomAdminSite(name='customadmin')
admin.site = custom_admin_site

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Register your model with the custom ModelAdmin class for the custom admin site
custom_admin_site.register(CustomUser, CustomUserAdmin)
# custom_admin_site.register(DashboardStatsCriteria)
# custom_admin_site.register(DashboardStats)
custom_admin_site.register(Student, StudentAdmin)
custom_admin_site.register(Parent, ParentAdmin)
custom_admin_site.register(Teacher, TeacherAdmin)
custom_admin_site.register(CourseCategory, CustomModelAdmin)
custom_admin_site.register(Course, CourseAdmin)
custom_admin_site.register(CourseSection, CustomModelAdmin)
custom_admin_site.register(Lesson, LessonAdmin)
custom_admin_site.register(Quiz, QuizAdmin)
custom_admin_site.register(Question, QuestionAdmin)
custom_admin_site.register(Choice, CustomModelAdmin)
custom_admin_site.register(ExamResult, ExamResultAdmin)
custom_admin_site.register(Subject, SubjectAdmin)
custom_admin_site.register(Syllabus, SyllabusAdmin)
custom_admin_site.register(LiveMeeting, LiveMeetingAdmin)
custom_admin_site.register(Class, ClassAdmin)
custom_admin_site.register(Section, SectionAdmin)
custom_admin_site.register(LessonPlan, LessonPlanAdmin)
custom_admin_site.register(Homework, HomeworkAdmin)
custom_admin_site.register(Payment, CustomModelAdmin)
custom_admin_site.register(QuestionChoice, CustomModelAdmin)
custom_admin_site.register(SubmitedHomworks, CustomModelAdmin)
custom_admin_site.register(ShoppingCart, CustomModelAdmin)
custom_admin_site.register(Order, CustomModelAdmin)
custom_admin_site.register(GeneralSettings, GeneralSettingsAdmin)
custom_admin_site.register(Countries, CountriesAdmin)
custom_admin_site.register(Role, RoleAdmin)
custom_admin_site.register(RolePermission, RolePermissionAdmin)
custom_admin_site.register(VideoLesson, VediolessonAdmin)
custom_admin_site.register(OnlineExam, OnlineExamAdmin)
custom_admin_site.register(StudentAttempt, CustomModelAdmin)
custom_admin_site.register(StudentAnswer, CustomModelAdmin)
custom_admin_site.register(StudentProgress, CustomModelAdmin)
custom_admin_site.register(Certificate, CustomModelAdmin)
custom_admin_site.register(Rating, RatingAdmin)
# custom_admin_site.register(CachedValue)


# Register the custom admin site
admin.site = custom_admin_site
