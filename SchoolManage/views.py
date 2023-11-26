from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token  # Import Token from Django Rest Framework
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from .permissions import IsTeacher  # Make sure to import the IsTeacher permission
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_protect
# Create viewsets for each model
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseSectionViewSet(viewsets.ModelViewSet):
    queryset = CourseSection.objects.all()
    serializer_class = CourseSectionSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SyllabusViewSet(viewsets.ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer

class LiveMeetingViewSet(viewsets.ModelViewSet):
    queryset = LiveMeeting.objects.all()
    serializer_class = LiveMeetingSerializer

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class LessonPlanViewSet(viewsets.ModelViewSet):
    queryset = LessonPlan.objects.all()
    serializer_class = LessonPlanSerializer

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

class OnlineExamViewSet(viewsets.ModelViewSet):
    queryset = OnlineExam.objects.all()
    serializer_class = OnlineExamSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class VideoLessonViewSet(viewsets.ModelViewSet):
    queryset = VideoLesson.objects.all()
    serializer_class = VideoLessonSerializer



# class StudentRegistrationView(generics.CreateAPIView):
#     serializer_class = StudentSerializer

#     def create(self, request, *args, **kwargs):
#         # Check if a user with the same username or email already exists
#         existing_user = CustomUser.objects.filter(username=request.data.get('username')).first()
#         if existing_user:
#             return Response({'error': 'User with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

#         # If the user doesn't exist, proceed with user creation
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         return Response({'message': 'User registration successful.'}, status=status.HTTP_201_CREATED)
from rest_framework.response import Response

class RegisterUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        else:
            print("Invalid data received:")
            print(request.data)
            print("Serializer errors:")
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])

def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        print(username,password)
        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
                print(user)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)
            print(user)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            print(token,user)
            return Response({'token': token.key ,'message': 'successful login' }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method in ['GET', 'POST']:
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






from .permissions import IsTeacher

class StudentListCreateView(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication]

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication]

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
from rest_framework import generics
from rest_framework.response import Response
from SchoolManage.models import Course, Teacher, CourseSection
from SchoolManage.serializers import CourseSerializer, CourseSectionSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTeacher  # Import your custom permission
from django.core.exceptions import PermissionDenied

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course
from .serializers import CourseWithSectionsQuizzesLessonsSerializer

@api_view(['POST'])
def create_course(request):
    try:
        # Get the authenticated user
        user = request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            serializer = CourseWithSectionsQuizzesLessonsSerializer(data=request.data)

            if serializer.is_valid():
                # Create the course and related sections, video lessons, quizzes, questions, and choices
                teacher = Teacher.objects.get(user=user)  # Get the teacher
                course = serializer.save(assign_teacher=teacher)

                return Response({'success': 'Course created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Only teachers can create courses.'}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsTeacher])
def get_course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        serialized_data = CourseWithContentSerializer(course)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        serializer = CourseWithSectionsQuizzesLessonsSerializer(course, data=request.data, partial=True)

        if serializer.is_valid():
            # Update the course and related sections, video lessons, quizzes, questions, and choices
            course = serializer.save()
            return Response({'success': 'Course updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['DELETE'])
def delete_course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        course.delete()
        return Response({'success': 'Course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course
from .serializers import CourseWithContentSerializer

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def list_courses_with_sections_and_lessons(request):
#     user = request.user
#     try:
#         teacher = Teacher.objects.get(user=user)
#         courses = Course.objects.filter(assign_teacher=teacher)

#         # Serialize the data using CourseWithContentSerializer
#         serialized_data = CourseWithContentSerializer(courses, many=True)

#         return Response(serialized_data.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseView(generics.ListAPIView):
    serializer_class = CourseWithContentSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    def get_queryset(self):
        # Add your logic here to specify the queryset
        # For example, to get courses assigned to the teacher:
        user = self.request.user
        if user.role == 'teacher':
            try:
                teacher = Teacher.objects.get(user=user)
                return Course.objects.filter(assign_teacher=teacher)
            except Teacher.DoesNotExist:
                pass

        # Return an empty queryset or handle other cases
        return Course.objects.none()  



# def index(request):
#      return render(request, '')
    
# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def home_data(request):
    # Fetch and prepare the data you need
    data = {
        "mainData": "Your main data here",
        "courseData": "Your course data here",
        "aboutUsData": "Your about us data here",
        "achievementData": "Your achievement data here",
        "experiencedData": "Your experienced data here",
    }
    return Response(data)





# class CourseCreateView(generics.CreateAPIView):
#     serializer_class = CourseSerializer
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated, IsTeacher]

#     def perform_create(self, serializer):
#      if self.request.user.role == 'teacher':
#         # Get or create a Teacher instance associated with the request.user
#         teacher_instance, _ = Teacher.objects.get_or_create(user=self.request.user)
        
#         # Set the assign_teacher explicitly to the teacher creating the course
#         serializer.save(assign_teacher=teacher_instance)
#      else:
#         raise PermissionDenied("User is not a teacher.")



# Remove the previous function-based view
# @api_view(['POST'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def courses(request):
#     if hasattr(request.user, 'teacher'):
#         request.data['assign_teacher'] = request.user.id
#         serializer = CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'detail': 'User is not a teacher.'}, status=status.HTTP_403_FORBIDDEN)

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher]


from rest_framework.authentication import BasicAuthentication

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Student


class CourseSectionsCreateView(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]

    queryset = CourseSection.objects.all()
    serializer_class = CourseSectionSerializer

from rest_framework.authentication import BasicAuthentication

class CourseSectionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]

    queryset = CourseSection.objects.all()
    serializer_class = CourseSectionSerializer
from rest_framework import generics
from .models import Quiz
from .serializers import QuizSerializer


class QuizCreateView(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    # queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        # Get the currently signed-in teacher
        teacher = Teacher.objects.get(user=self.request.user)
        
        # Fetch all courses assigned to the teacher
        assigned_courses = Course.objects.filter(assign_teacher=teacher)
        
        # Filter quizzes by courses assigned to the teacher
        return Quiz.objects.filter(course__in=assigned_courses)
    def perform_create(self, serializer):
    # Get the currently signed-in teacher
     teacher = Teacher.objects.get(user=self.request.user)
     print("Teacher ID:", teacher.id)

    # Get the course ID from the request data
     course_id = self.request.data.get('course')
     print("Course ID:", course_id)
 
    # Check if the course is assigned to the teacher
     if Course.objects.filter(pk=course_id, assign_teacher=teacher).exists():
        # If the course is assigned to the teacher, create the quiz
        serializer.save()
     else:
        # If the course is not assigned to the teacher, raise a permission denied exception
        raise PermissionDenied("You don't have permission to create a quiz for this course.")


class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer



class QuestionsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionsView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Question.objects.all()


class ChoicesView(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Choice.objects.all()


class choicesDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class QuestionChoicesView(generics.ListCreateAPIView):
    serializer_class = QuestionChoiceSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = QuestionChoice.objects.all()


class QuestionChoicesDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer


class LivemeetingView(generics.ListCreateAPIView):
    serializer_class = LiveMeetingSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            try:
                # If the user is a teacher, try to fetch the associated teacher profile
                teacher = Teacher.objects.get(user=user)

                # Filter LiveMeetings organized by the teacher's related user
                return LiveMeeting.objects.filter(Organizer=teacher.user)
            except Teacher.DoesNotExist:
                pass

        # Handle cases where the user is not a teacher or teacher profile doesn't exist
        return LiveMeeting.objects.none()

    def perform_create(self, serializer):
        # Automatically set the organizer to the user who created the meeting
        serializer.save(Organizer=self.request.user)

    def create(self, request, *args, **kwargs):
        # Override the create method to set the organizer and return a response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class LessonView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            try:
                # If the user is a teacher, try to fetch the associated teacher profile
                teacher = Teacher.objects.get(user=user)

                # Filter homeworks related to the teacher
                return Lesson.objects.filter(teacher=teacher)
            except Teacher.DoesNotExist:
                pass

        # Handle cases where the user is not a teacher or teacher profile doesn't exist
        return Lesson.objects.none()

    def perform_create(self, serializer):
        # Automatically set the teacher to the user who created the homework
        user = self.request.user
        teacher = Teacher.objects.get(user=user)  # Assuming each teacher has one associated user
        serializer.save(teacher=teacher)

    def create(self, request, *args, **kwargs):
        # Override the create method to set the teacher and return a response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LivemeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LiveMeetingSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            try:
                # If the user is a teacher, try to fetch the associated teacher profile
                teacher = Teacher.objects.get(user=user)

                # Filter LiveMeetings organized by the teacher's related user
                return LiveMeeting.objects.filter(Organizer=teacher.user)
            except Teacher.DoesNotExist:
                pass

        # Handle cases where the user is not a teacher or teacher profile doesn't exist
        return LiveMeeting.objects.none()

    def perform_create(self, serializer):
        # Automatically set the organizer to the user who created the meeting
        serializer.save(Organizer=self.request.user)

    def create(self, request, *args, **kwargs):
        # Override the create method to set the organizer and return a response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            try:
                # If the user is a teacher, try to fetch the associated teacher profile
                teacher = Teacher.objects.get(user=user)

                # Filter homeworks related to the teacher
                return Lesson.objects.filter(teacher=teacher)
            except Teacher.DoesNotExist:
                pass

        # Handle cases where the user is not a teacher or teacher profile doesn't exist
        return Lesson.objects.none()

    def perform_create(self, serializer):
        # Automatically set the teacher to the user who created the homework
        user = self.request.user
        teacher = Teacher.objects.get(user=user)  # Assuming each teacher has one associated user
        serializer.save(teacher=teacher)

    def create(self, request, *args, **kwargs):
        # Override the create method to set the teacher and return a response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ExamResultView(generics.ListCreateAPIView):
    serializer_class = ExamResultSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = ExamResult.objects.all()

    
class LessonPlanView(generics.ListCreateAPIView):
    serializer_class = LessonPlanSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            try:
                # If the user is a teacher, try to fetch the associated teacher profile
                teacher = Teacher.objects.get(user=user)

                # Filter homeworks related to the teacher
                return LessonPlan.objects.filter(teacher=teacher)
            except Teacher.DoesNotExist:
                pass

        # Handle cases where the user is not a teacher or teacher profile doesn't exist
        return LessonPlan.objects.none()

    def perform_create(self, serializer):
        # Automatically set the teacher to the user who created the homework
        user = self.request.user
        teacher = Teacher.objects.get(user=user)  # Assuming each teacher has one associated user
        serializer.save(teacher=teacher)

    def create(self, request, *args, **kwargs):
        # Override the create method to set the teacher and return a response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LessonPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonPlanSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            try:
                # If the user is a teacher, try to fetch the associated teacher profile
                teacher = Teacher.objects.get(user=user)

                # Filter homeworks related to the teacher
                return LessonPlan.objects.filter(teacher=teacher)
            except Teacher.DoesNotExist:
                pass

        # Handle cases where the user is not a teacher or teacher profile doesn't exist
        return LessonPlan.objects.none()

    def perform_create(self, serializer):
        # Automatically set the teacher to the user who created the homework
        user = self.request.user
        teacher = Teacher.objects.get(user=user)  # Assuming each teacher has one associated user
        serializer.save(teacher=teacher)

    def create(self, request, *args, **kwargs):
        # Override the create method to set the teacher and return a response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class HomeworkView(generics.ListCreateAPIView):
    serializer_class = HomeworkSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            try:
                # If the user is a teacher, try to fetch the associated teacher profile
                teacher = Teacher.objects.get(user=user)

                # Filter homeworks related to the teacher
                return Homework.objects.filter(teacher=teacher)
            except Teacher.DoesNotExist:
                pass

        # Handle cases where the user is not a teacher or teacher profile doesn't exist
        return Homework.objects.none()

    def perform_create(self, serializer):
        # Automatically set the teacher to the user who created the homework
        user = self.request.user
        teacher = Teacher.objects.get(user=user)  # Assuming each teacher has one associated user
        serializer.save(teacher=teacher)

    def create(self, request, *args, **kwargs):
        # Override the create method to set the teacher and return a response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class HomeworkDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HomeworkSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            try:
                # If the user is a teacher, try to fetch the associated teacher profile
                teacher = Teacher.objects.get(user=user)

                # Filter homeworks related to the teacher
                return Homework.objects.filter(teacher=teacher)
            except Teacher.DoesNotExist:
                pass

        # Handle cases where the user is not a teacher or teacher profile doesn't exist
        return Homework.objects.none()

    def perform_create(self, serializer):
        # Automatically set the teacher to the user who created the homework
        user = self.request.user
        teacher = Teacher.objects.get(user=user)  # Assuming each teacher has one associated user
        serializer.save(teacher=teacher)

    def create(self, request, *args, **kwargs):
        # Override the create method to set the teacher and return a response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ExamResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExamResultSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = ExamResult.objects.all()

class SubjectView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated,IsTeacher]
    queryset = Subject.objects.all()

class SyllabusView(generics.ListAPIView):
    serializer_class = SyllabusSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated,IsTeacher]
    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            # If the user is a teacher, fetch the associated teacher profile
            teacher = Teacher.objects.get(user=user)

            # Filter syllabus based on courses assigned to the teacher
            assigned_courses = Course.objects.filter(assign_teacher=teacher)
            return Syllabus.objects.filter(course__in=assigned_courses)
        else:
            # Handle cases where the user is not a teacher
            return Syllabus.objects.none()  # Return an empty queryset or handle the error as needed
class SyllabusStudentDetailView(generics.RetrieveAPIView):
    serializer_class = SyllabusSerializer
    authentication_classes = [BasicAuthentication]
    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            # If the user is a teacher, fetch the associated teacher profile
            teacher = Teacher.objects.get(user=user)

            # Filter syllabus based on courses assigned to the teacher
            assigned_courses = Course.objects.filter(assign_teacher=teacher)
            return Syllabus.objects.filter(course__in=assigned_courses)
        else:
            # Handle cases where the user is not a teacher
            return Syllabus.objects.none()  # Return an empty queryset or handle the error as needed

class SubmitedHomworksView(generics.ListAPIView):
    serializer_class = SubmitedHomworksSerializer  # Replace with your actual serializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            try:
                # If the user is a teacher, try to fetch the associated teacher profile
                teacher = Teacher.objects.get(user=user)

                # Filter submitted homeworks related to the teacher's homeworks
                return SubmitedHomworks.objects.filter(Homework__teacher=teacher)
            except Teacher.DoesNotExist:
                pass

        # Handle cases where the user is not a teacher or teacher profile doesn't exist
        return SubmitedHomworks.objects.none()



class OnlineExamView(generics.ListCreateAPIView):
    serializer_class = OnlineExamSerializer
    authentication_classes=[BasicAuthentication]
    permission_classes = [IsAuthenticated,IsTeacher]
    
    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            try:
                # If the user is a teacher, try to fetch the associated teacher profile
                teacher = Teacher.objects.get(user=user)

                # Filter homeworks related to the teacher
                return OnlineExam.objects.filter(teacher=teacher)
            except Teacher.DoesNotExist:
                pass

        # Handle cases where the user is not a teacher or teacher profile doesn't exist
        return OnlineExam.objects.none()

    def perform_create(self, serializer):
        # Automatically set the teacher to the user who created the homework
        user = self.request.user
        teacher = Teacher.objects.get(user=user)  # Assuming each teacher has one associated user
        serializer.save(teacher=teacher)

    def create(self, request, *args, **kwargs):
        # Override the create method to set the teacher and return a response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class OnlineExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OnlineExamSerializer
    authentication_classes=[BasicAuthentication]
    permission_classes = [IsAuthenticated,IsTeacher]

    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Ensure the user has the 'teacher' role
        if user.role == 'teacher':
            try:
                # If the user is a teacher, try to fetch the associated teacher profile
                teacher = Teacher.objects.get(user=user)

                # Filter homeworks related to the teacher
                return OnlineExam.objects.filter(teacher=teacher)
            except Teacher.DoesNotExist:
                pass

        # Handle cases where the user is not a teacher or teacher profile doesn't exist
        return OnlineExam.objects.none()

    def perform_create(self, serializer):
        # Automatically set the teacher to the user who created the homework
        user = self.request.user
        teacher = Teacher.objects.get(user=user)  # Assuming each teacher has one associated user
        serializer.save(teacher=teacher)

    def create(self, request, *args, **kwargs):
        # Override the create method to set the teacher and return a response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



# class CourseWithQuizAndQuestionsView(generics.ListCreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

#     def create(self, request, *args, **kwargs):
#         course_data = request.data.get('course')
#         quiz_data = request.data.get('quiz')
#         questions_data = request.data.get('questions')
#         print(request.data)
#         # Validate course data
#         course_serializer = CourseSerializer(data=course_data)
#         if not course_serializer.is_valid():
#             return Response(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         # Validate quiz data
#         quiz_serializer = QuizSerializer(data=quiz_data)
#         if not quiz_serializer.is_valid():
#             return Response(quiz_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Save course and quiz
#         course = course_serializer.save()
#         quiz = quiz_serializer.save(course=course)

#         # Process and save questions
#         for question_data in questions_data:
#             question_data['quiz'] = quiz.id  # Link the question to the quiz
#             question_serializer = QuestionSerializer(data=question_data)
#             if question_serializer.is_valid():
#                 question_serializer.save()
#             else:
#                 return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'message': 'Course, quiz, questions, and choices created successfully.'}, status=status.HTTP_201_CREATED)


# class QuizAndQuestionsCreateView(generics.ListCreateAPIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated, IsTeacher]
#     queryset = Quiz.objects.none()
#     serializer_class = QuizAndQuestionCreateSerializer  # Assign the combined serializer

#     def create(self, request, *args, **kwargs):
#         # Deserialize the combined data
#         combined_serializer = self.get_serializer(data=request.data)

#         if combined_serializer.is_valid():
#             # Extract and create the quiz data
#             quiz_data = combined_serializer.validated_data['quiz']
#             quiz_serializer = QuizSerializer(data=quiz_data)
#             if quiz_serializer.is_valid():
#                 quiz = quiz_serializer.save()

#                 # Extract and create the questions data
#                 questions_data = combined_serializer.validated_data['questions']
#                 question_instances = []

#                 for question_data in questions_data:
#                     question_data['quiz'] = quiz.id
#                     question_serializer = QuestionSerializer(data=question_data)

#                     if question_serializer.is_valid():
#                         question_instance = question_serializer.save()
#                         question_instances.append(question_instance)
#                     else:
#                         # If a question is invalid, rollback the quiz creation and return an error
#                         quiz.delete()
#                         return Response({'detail': 'Error creating questions.'}, status=status.HTTP_400_BAD_REQUEST)

#                 return Response({'quiz': quiz_serializer.data, 'questions': [qs.data for qs in question_instances]}, status=status.HTTP_201_CREATED)

#             return Response(quiz_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response(combined_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import your serializer for the function
# from .serializers import CourseContentSerializer

# Import the create_course_with_sections_quizzes_lessons function
from rest_framework import generics
from .serializers import CourseWithSectionsQuizzesLessonsSerializer
from .utils import create_course_with_sections_quizzes_lessons

class CreateCourseWithSectionsQuizzesLessonsView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseWithSectionsQuizzesLessonsSerializer

    def create(self, request, *args, **kwargs):
        serializer = CourseWithSectionsQuizzesLessonsSerializer(data=request.data)

        if serializer.is_valid():
            response = create_course_with_sections_quizzes_lessons(serializer.validated_data)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from django.shortcuts import render, redirect
# from .models import Role

# def add_role(modeladmin, request, queryset):
#     if request.method == 'POST':
#         role_name = request.POST.get('name')
#         if role_name:
#             Role.objects.create(name=role_name)
#             return redirect('admin:SchoolManage_role_changelist')  # Redirect to the list view

#     return render(request, 'admin/add_role_form.html')


# def index(request):
#     return render(request, "build/index.html")
from rest_framework.views import APIView
class GeneralSettingsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            general_settings = GeneralSettings.objects.first()
            serializer = GeneralSettingsSerializer(general_settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GeneralSettings.DoesNotExist:
            return Response({"detail": "GeneralSettings not found"}, status=status.HTTP_404_NOT_FOUND)

class CountryListView(APIView):
    def get(self, request, *args, **kwargs):
        countries = Countries.objects.all()
        serializer = CountriesSerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)