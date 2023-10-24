from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'telephone', 'gender', 'birthday', 'address', 'marital_status')
    list_filter = ('role', 'gender', 'marital_status')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'telephone')

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
# admin.site.register(Rating)
