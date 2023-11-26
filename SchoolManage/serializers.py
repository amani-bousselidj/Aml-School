from rest_framework import serializers
from .models import *
class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'
# serializers.py
class CustomUserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(write_only=True)
    country_id = serializers.IntegerField(write_only=True, required=False)

    
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'role_name', 'country_id','profile_picture')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role_name = validated_data.pop('role_name', None)
        country_id = validated_data.pop('country_id', None)

        if role_name:
            roles = Role.objects.filter(name=role_name)
            if roles.exists():
                role = roles.first()
                validated_data['role'] = role
            else:
                raise serializers.ValidationError(f"Role with name '{role_name}' does not exist.")

        if country_id:
            country = Countries.objects.get(pk=country_id)
            validated_data['country'] = country

        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'



# class CourseSectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourseSection
#         fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'
class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'
class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = '__all__'

    

class QuizAndQuestionCreateSerializer(serializers.Serializer):
    quiz = QuizSerializer()
    questions = QuestionSerializer(many=True)

# class CourseContentSerializer(serializers.ModelSerializer):
#     sections = CourseSectionSerializer(many=True, read_only=True)

#     class Meta:
#         model = Course
#         fields = '__all__'



class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = '__all__'
class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syllabus
        fields = '__all__'

class LiveMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveMeeting
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class LessonPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        fields = '__all__'

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'

class OnlineExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineExam
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class SubmitedHomworksSerializer(serializers.ModelSerializer):

     class Meta:
        model = SubmitedHomworks
        fields = '__all__'

class VideoLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLesson
        fields = '__all__'

class CourseSectionSerializer(serializers.ModelSerializer):
    video_lessons = VideoLessonSerializer(many=True, required=False)
    quiz = QuizSerializer(required=False)


    class Meta:
        model = CourseSection
        fields = '__all__'


from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    sections = CourseSectionSerializer(many=True)  # Assuming you have a CourseSectionSerializer

    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Check if the course is free, and if so, exclude price and discount
        if data['is_free']:
            data.pop('price')
            data.pop('discount')
        return data
class CourseWithSectionsQuizzesLessonsSerializer(serializers.ModelSerializer):
    sections = CourseSectionSerializer(many=True, required=False)

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        sections_data = validated_data.pop('sections', [])
        course = Course.objects.create(**validated_data)

        for section_data in sections_data:
            video_lessons_data = section_data.pop('video_lessons', [])
            quiz_data = section_data.pop('quiz', None)

            section = CourseSection.objects.create(course=course, **section_data)

            for video_lesson_data in video_lessons_data:
                VideoLesson.objects.create(course=course, section=section, **video_lesson_data)

            if quiz_data:
                questions_data = quiz_data.pop('questions', [])
                quiz = Quiz.objects.create(course=course, section=section, **quiz_data)

                for question_data in questions_data:
                    choices_data = question_data.pop('choices', [])
                    question = Question.objects.create(quiz=quiz, **question_data)

                    for choice_data in choices_data:
                        Choice.objects.create(question=question, **choice_data)

        return course

from rest_framework import serializers
class CourseWithContentSerializer(serializers.ModelSerializer):
    sections = CourseSectionSerializer(many=True, source='coursesection_set')
  
    class Meta:
        model = Course
        fields = '__all__'


class GeneralSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralSettings
        fields = '__all__'