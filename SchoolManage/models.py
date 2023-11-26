from django.db import models
from django.contrib.auth.models import AbstractUser, Permission as AuthPermission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
import uuid
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

class Role(models.Model):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Parent', 'Parent'),
    ]

    name = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        blank=True,
                verbose_name='Role',  # Add verbose name for 'name'
    )

    custom_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
                verbose_name='Custom Role',  # Add verbose name for 'custom_name'
    )
    
    def save(self, *args, **kwargs):
        if not self.name and self.custom_name:
            self.name = self.custom_name
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        return self.custom_name or self.name or str(self.pk)

    class Meta:
        verbose_name = _("Role & Permissions")
        verbose_name_plural = _("Roles & Permissions")
        





    

class Countries(models.Model):
    name = models.CharField(max_length=50)
    Date_Created = models.DateField(auto_now=False, auto_now_add=False)
    countrie_flag = models.ImageField(upload_to='countries_flags/', height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('Female', 'Female'),
    ]

    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    telephone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birthday = models.DateField(default=None, blank=True, null=True)
    address = models.TextField(default=None, blank=True, null=True)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)

    @property
    def teacher(self):
        try:
            return self.teacher_profile
        except Teacher.DoesNotExist:
            return None

    @property
    def student(self):
        try:
            return self.student_profile
        except Student.DoesNotExist:
            return None

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role:
        try:
            role = instance.role  # Use the role directly, assuming it's already assigned correctly
            print(f"Role found: {role}")
            
            if role.name == 'Teacher':
                Teacher.objects.create(user=instance)
            elif role.name == 'Student':
                Student.objects.create(user=instance)
        except Role.DoesNotExist:
            print(f"Role with name '{instance.role_name}' does not exist.")



@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.role:
        if instance.role.name == 'Teacher':
            instance.teacher.save()
        elif instance.role.name == 'Student':
            instance.student.save()

class CustomPermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, default=None)
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE, null=True, default=None)
    can_view = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_change = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.model_name} - {self.role.name}'

    class Meta:
        verbose_name = _("Custom Permission")
        verbose_name_plural = _("Custom Permissions")


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')
        verbose_name = _("Role Permission")
        verbose_name_plural = _("Role Permissions")

class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    Parent_name = models.CharField(max_length=255, blank=True, null=True)
    Parent_phone = models.CharField(max_length=15, blank=True, null=True)
    Parent_occupation = models.CharField(max_length=255, blank=True, null=True)
    # children = models.ManyToManyField(CustomUser, related_name='parents',        limit_choices_to={'role__name__exact': 'student'})

    def __str__(self):
        return self.Parent_name or str(self.user)

    class Meta:
        verbose_name = _("Parent")
        verbose_name_plural = _("Parents")

class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('Female', 'Female'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    admission_number = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    student_name = models.CharField(max_length=255)
    class_name = models.CharField(max_length=50)
    birthday = models.DateField(default=None,null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    mobile_phone_number = models.CharField(max_length=15)
    parents = models.ManyToManyField(Parent)
    # Date_joined = models.DateField( auto_now=False, auto_now_add=False,default=None,null=True)
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")




class Teacher(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('Female', 'Female'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    personnel_id = models.CharField(max_length=20, blank=True, null=True)
    role_teacher = models.CharField(max_length=50, blank=True)
    designation_faculty = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type_of_contract = models.CharField(max_length=50, blank=True, null=True)
    work_shift = models.CharField(max_length=50, blank=True, null=True)
    work_location = models.CharField(max_length=100, blank=True, null=True)
    registration_date = models.DateField(null=True)
    barcode = models.CharField(max_length=20, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=10, null=True, choices=GENDER_CHOICES)
    birthday = models.DateField(blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")


class CourseCategory(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = _("Course Category")
        verbose_name_plural = _("Course Categories")


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=None)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)
    lesson_type = models.CharField(max_length=20, choices=[('video', 'Video'), ('pdf', 'PDF'), ('text', 'Text'), ('document', 'Document')])
    video_provider = models.CharField(max_length=20, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    inline_preview_image = models.ImageField(upload_to='lesson_images/')
    summary_of_lesson = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='course_covers/')
    class_or_level = models.CharField(max_length=50)
    assign_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, default=None)
    course_preview_url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_free = models.BooleanField()
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    visibility = models.BooleanField()

    def get_sections(self):
        return CourseSection.objects.filter(course=self)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")


class VideoLesson(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration = models.PositiveIntegerField(blank=True, null=True)
    summary = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Video Lesson")
        verbose_name_plural = _("Video Lessons")


class CourseSection(models.Model):
    section_title = models.CharField(max_length=100)
    lessons = models.ManyToManyField('Lesson', through='LessonOrder', blank=True)
    quiz = models.OneToOneField('Quiz', on_delete=models.CASCADE, blank=True, null=True)
    video_lessons = models.ManyToManyField('VideoLesson', blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.section_title

    class Meta:
        verbose_name = _("Course Section")
        verbose_name_plural = _("Course Sections")


class LessonOrder(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    course_section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Lesson: {self.lesson.title}, Section: {self.course_section.section_title}"

    class Meta:
        verbose_name = _("Lesson Order")
        verbose_name_plural = _("Lesson Orders")


class Choice(models.Model):
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"Question: {self.question.question_text}, Choice: {self.choice.choice_text}"

    class Meta:
        verbose_name = _("Question Choice")
        verbose_name_plural = _("Question Choices")


class Syllabus(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    syllabus_status = models.IntegerField()

    def __str__(self):
        return f"{self.course} - {self.Student}"

    class Meta:
        verbose_name = _("Syllabus")
        verbose_name_plural = _("Syllabi")


class LiveMeeting(models.Model):
    meeting_title = models.CharField(max_length=255)
    meeting_date_time = models.DateTimeField()
    meeting_url = models.URLField
    Organizer = models.ForeignKey(CustomUser,  on_delete=models.CASCADE,default=None,null=True)
    def __str__(self):
        return self.meeting_title
    class Meta:
        verbose_name = _("LiveMeeting")
        verbose_name_plural = _("LiveMeetings")

class Class(models.Model):
    class_name = models.CharField(max_length=50)
    def __str__(self):
        return self.class_name
    
    class Meta:
        verbose_name = _("Class")
        verbose_name_plural = _("Classes")
   
class Section(models.Model):
    section_name = models.CharField(max_length=50)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    def __str__(self):
        return self.section_name
    class Meta:
        verbose_name = _("Section")
        verbose_name_plural = _("Sections")
class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    exam_title = models.CharField(max_length=255)
    date = models.DateField()
    result = models.DecimalField(max_digits=5, decimal_places=2)
    section_name = models.ForeignKey(Section, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        student_name = self.student.student_name if self.student else "Unknown Student"
        return f"{student_name} - {self.exam_title}"

    class Meta:
        verbose_name = _("ExamResult")
        verbose_name_plural = _("ExamResults")
class LessonPlan(models.Model):
    lesson = models.ForeignKey(Lesson,  on_delete=models.CASCADE,default=None,blank=True,null=True)
    topic = models.CharField(max_length=255)
    date = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    lecture_youtube_url = models.URLField(default=None,blank=True)
    attachment = models.FileField(upload_to='lesson_plan_attachments/',blank=True)
    lecture_video = models.FileField(upload_to='lesson_plan_lecture_videos/',blank=True)
    general_objectives = models.TextField()
    presentation_text_area = models.TextField()
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE,default=None,blank=True,null=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,default=None,blank=True,null=True)
    section_name = models.ForeignKey(Section, on_delete=models.CASCADE,default=None,blank=True,null=True)
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE,default=None,blank=True)
    def __str__(self):
        return self.topic
    class Meta:
        verbose_name = _("LessonPlan")
        verbose_name_plural = _("LessonPlans")
class Homework(models.Model):
    teacher= models.ForeignKey(Teacher, on_delete=models.CASCADE,default=None,blank=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    section= models.ForeignKey(Section, on_delete=models.CASCADE,default=None,blank=True,null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,default=None)
    homework_date = models.DateField()
    submission_date = models.DateField()
    document = models.FileField(upload_to='homework_documents/')
    description = models.TextField()
    def __str__(self):
        return f"{self.subject} - {self.homework_date}"
    class Meta:
        verbose_name = _("Homework")
        verbose_name_plural = _("Homeworks")
class SubmitedHomworks(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Homework =models.ForeignKey(Homework, on_delete=models.CASCADE)
    attachement = models.FileField(upload_to='students_homework_documents/')
    SubmissionDate = models.DateField()
    class Meta:
        verbose_name = _("SubmitedHomwork")
        verbose_name_plural = _("SubmitedHomworks")
class OnlineExam(models.Model):
    teacher= models.ForeignKey(Teacher, on_delete=models.CASCADE,default=None,blank=True)

    exam_title = models.CharField(max_length=255)
    exam_from_date = models.DateField()
    exam_to_date = models.DateField()
    auto_result_publish_date = models.DateTimeField()
    time_duration = models.DurationField()
    attempt = models.IntegerField()
    description = models.TextField()
    def __str__(self):
        return self.exam_title


    def __str__(self):
        return f"{self.student} - {self.date_of_payment}"
    
    class Meta:
        verbose_name = _("OnlineExam")
        verbose_name_plural = _("OnlineExams")
class StudentAttempt(models.Model):
    quizz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="attempts"
    )
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="attempts"
    )
    score = models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name = _("StudentAttempt")
        verbose_name_plural = _("StudentAttempts")
class StudentAnswer(models.Model):
    attempt = models.ForeignKey(
        StudentAttempt, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.ForeignKey(
        Choice, on_delete=models.CASCADE, related_name="answer"
    )
    class Meta:
        verbose_name = _("StudentAnswer")
        verbose_name_plural = _("StudentAnswers")

class StudentProgress(models.Model):
    user: CustomUser = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    course: Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    disabled = models.BooleanField(default=False)

    last_video_index = models.SmallIntegerField(default=0)
    last_chapter_index = models.SmallIntegerField(default=0)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"StudentProgress {self.user.username} - {self.course.title}"
    
    class Meta:
        verbose_name = _("StudentProgress")
        verbose_name_plural = _("StudentProgresses")

class Certificate(models.Model):
    user: CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course: Course = models.ForeignKey(Course, on_delete=models.CASCADE)

    certificate_image = models.ImageField(upload_to='certificate_upload_dir/')

    # def generate(self, user, course):
    #     certificate_image = generate_certificate(
    #         f"{user.first_name} {user.last_name}", course.title
    #     )
    #     certificate_image.save(f"/tmp/certificate-{user.username}.png")
    #     self.user = user
    #     self.course = course
    #     self.certificate_image.save(
    #         name="certificate.png",
    #         content=open(f"/tmp/certificate-{user.username}.png", "rb"),
    #         save=True,
    #     )
    #     self.save()

    class Meta:
        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")

class Rating(models.Model):
     student: CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
     video: Course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="ratings"
    )

     rating = models.FloatField(default=0)

     def __str__(self):
         return f'{self.student} * {self.video}'
     
     def display_star_rating(self):
      full_stars = int(self.rating)  # Number of full stars
      remainder = self.rating - full_stars  # Fractional part for half stars

      full_star_rating = "★" * full_stars
      half_star_rating = "½" if remainder >= 0.5 else ""  # Display half star if remainder is 0.5 or more

      return full_star_rating + half_star_rating

     class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")

class Order(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_issued = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Order {self.pk} {self.buyer.username}-{self.course.title}'
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

class Payment(models.Model):
    PENDING = 'p'
    ACCEPTED = 'a'
    REFUSED = 'r'

    STATUS_CHOICES = [
        (PENDING, _('Pending')),
        (ACCEPTED, _('Accepted')),
        (REFUSED, _('Refused')),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE,default=None)
    # receipt = models.FileField(upload_to=get_payment_upload_path)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f'{self.order.__str__()} Payment'
    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payment")
class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE,default=None)
    courses = models.ManyToManyField(Course)
    Date_create= models.DateField(auto_now=True)
    def __str__(self):
        return f'{self.user} Cart'
    class Meta:
        verbose_name = _("ShoppingCart")
        verbose_name_plural = _("ShoppingCarts")
from django.conf import settings
class GeneralSettings(models.Model):
    site_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    snapchat = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    work_time = models.IntegerField(blank=True, null=True)
    google_map_link = models.URLField(blank=True, null=True)
    google_map_iframe = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    login_timeout = models.PositiveIntegerField(blank=True, null=True)
    about_small = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True)
    seo_keywords = models.TextField(blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    privacy_policy = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    head_tag = models.TextField(blank=True, null=True)
    footer_tag = models.TextField(blank=True, null=True)
    logo_changed = False  # Variable to indicate whether the logo has changed

    def save(self, *args, **kwargs):
        if self.pk:
            original = GeneralSettings.objects.get(pk=self.pk)
            if original.logo != self.logo:
                self.logo_changed = True  # Set the variable to True if the logo has changed

        super().save(*args, **kwargs)

    def get_custom_logo_url(self):
        if self.logo and self.logo_changed:
            # If the logo has changed, return the updated logo URL
            return self.logo.url
        elif self.logo:
            # If the logo has not changed, return the original logo URL
            return self.logo.url
        else:
            # If there is no logo, return a default logo URL or handle accordingly
            return settings.STATIC_URL + 'admin/img/default_logo.png'  # Adjust this line as needed

    class Meta:
        verbose_name = _("GeneralSetting")
        verbose_name_plural = _("GeneralSettings")

    def __str__(self):
        return "General Settings"
class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    service_name = models.ForeignKey(ContentType, on_delete=models.CASCADE,default=None,null=True)
    can_view = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_change = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    def __str__(self) :
        return f'{self.service_name.model}'
    class Meta:
        verbose_name = _("Permission")
        verbose_name_plural = _("Permissions")
    def get_service_name(self):
        return self.service_name
    @receiver(post_save, sender=Role)
    def extend_permissions(sender, instance, **kwargs):
     if instance.name in ['Student', 'Teacher', 'Parent']:
        # Copy default permissions for Student, Teacher, Parent
        default_permissions = RolePermission.objects.filter(role__name=instance.name)
        for permission in default_permissions:
            RolePermission.objects.get_or_create(
                role=instance,
                service_name=permission.service_name,
                can_view=permission.can_view,
                can_add=permission.can_add,
                can_change=permission.can_change,
                can_delete=permission.can_delete
            )

from django.contrib.contenttypes.models import ContentType
from django.db import models

class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    service_name = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='permissions_for_service')
    can_view = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_change = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.role.name}-Permissions'
    def get_service_name(self):
        return self.service_name.model 
    class Meta:
        verbose_name = _("Permission")
        verbose_name_plural = _("Permissions")

    


class UICustomization(models.Model):
    code_snippet = models.TextField()



    