# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views
# from .views import *
# from rest_framework.authtoken.views import obtain_auth_token
# # Create a router
# router = DefaultRouter()

# # Register viewsets for your models
# router.register(r'customusers', views.CustomUserViewSet)
# # router.register(r'students', views.StudentViewSet)
# router.register(r'parents', views.ParentViewSet)
# router.register(r'teachers', views.TeacherViewSet)
# router.register(r'coursecategories', views.CourseCategoryViewSet)
# # router.register(r'courses', views.CourseViewSet)
# router.register(r'coursesections', views.CourseSectionViewSet)
# router.register(r'lessons', views.LessonViewSet)
# router.register(r'quizzes', views.QuizViewSet)
# router.register(r'questions', views.QuestionViewSet)
# router.register(r'choices', views.ChoiceViewSet)
# router.register(r'examresults', views.ExamResultViewSet)
# router.register(r'subjects', views.SubjectViewSet)
# router.register(r'syllabi', views.SyllabusViewSet)
# router.register(r'livemeetings', views.LiveMeetingViewSet)
# router.register(r'classes', views.ClassViewSet)
# router.register(r'sections', views.SectionViewSet)
# router.register(r'lessonplans', views.LessonPlanViewSet)
# router.register(r'homeworks', views.HomeworkViewSet)
# router.register(r'onlineexams', views.OnlineExamViewSet)
# router.register(r'payments', views.PaymentViewSet)

# # Define your API URLs
# urlpatterns = [
#     path('', include(router.urls)),
    # path('api/student/register/', StudentRegistrationView.as_view(), name='student-register'),
# # Other paths...
#     path('create_course_with_sections_quizzes_lessons/', CreateCourseWithSectionsQuizzesLessonsView.as_view(), name='create_course_with_sections_quizzes_lessons'),                                                        
#     # path('students/', views.student_list, name='student-list'),
#     # path('courses/', views.courses, name='courses'),
#     # path('course/', CourseCreateView.as_view(), name='course'),
    
#     path('courses/', CourseView.as_view(), name='courses'),
#     # path('api/create_course_with_sections_quizzes_lessons/', CreateCourseWithSectionsQuizzesLessonsView.as_view(), name='create_course_with_sections_quizzes_lessons'),

#     path('CourseSection/', CourseSectionsCreateView.as_view(), name='CourseSection'),
#     path('CourseSection/<int:pk>/', CourseSectionsDetailView.as_view(), name='CourseSection-detail'),
#     path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-details'),
#     path('Quiz/<int:pk>/', QuizDetail.as_view(), name='QuizDetail'),
#     path('Quiz/', QuizCreateView.as_view(), name='Quiz'),
#     path('Questions/', QuestionsView.as_view(), name='Questions'),
#     path('Livemeeting/', LivemeetingView.as_view(), name='Livemeeting'),
#     path('Choices/', ChoicesView.as_view(), name='Choices'),
#     path('Lessons/', LessonView.as_view(), name='Lessons'),
#     path('Homeworks/', HomeworkView.as_view(), name='Homeworks'),
#     path('ExamResult/', ExamResultView.as_view(), name='ExamResult'),
#     path('QuestionChoices/', QuestionChoicesView.as_view(), name='QuestionChoices'),
#    
#    
#     path('Questions/<int:pk>/', QuestionsDetailsView.as_view(), name='Question-details'),
#     path('QuestionChoices/<int:pk>/', QuestionChoicesDetailsView.as_view(), name='QuestionChoices-details'),
#     path('Choices/<int:pk>/', choicesDetailsView.as_view(), name='Choice-details'),
#     path('Lessons/<int:pk>/', LessonDetailView.as_view(), name='Lessons-details'),
#     # path('QuizAndQuestions/', QuizAndQuestionsCreateView.as_view(), name='QuizAndQuestions-details'),
#         # path('course_with_quiz_and_questions/', CourseWithQuizAndQuestionsView.as_view(), name='course_with_quiz_and_questions'),
#     # path('create_course_with_sections_and_content/', CreateCourseWithSectionsAndContentView.as_view(), name='create-course'),
#    
#     # Remove the 'student-create' pattern
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views
from .views import *

# Create a router for the Course model
router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)

# Create a nested router for CourseSections
course_sections_router = routers.NestedDefaultRouter(router, r'courses', lookup='course')
course_sections_router.register(r'sections', views.CourseSectionViewSet, basename='course-section')

# Create a nested router for VideoLessons
video_lessons_router = routers.NestedDefaultRouter(course_sections_router, r'sections', lookup='course_section')
video_lessons_router.register(r'videolessons', views.VideoLessonViewSet, basename='video-lesson')

# Create a nested router for Quizzes
quizzes_router = routers.NestedDefaultRouter(course_sections_router, r'sections', lookup='course_section')
quizzes_router.register(r'quizzes', views.QuizViewSet, basename='quiz')

# Create a nested router for Questions
questions_router = routers.NestedDefaultRouter(quizzes_router, r'quizzes', lookup='quiz')
questions_router.register(r'questions', views.QuestionViewSet, basename='question')

urlpatterns = [
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('Homeworks/<int:pk>/', HomeworkDetailView.as_view(), name='Homework-details'),
    path('LessonPlan/<int:pk>/', LessonPlanDetailView.as_view(), name='LessonPlan-details'),
    path('Syllabus/', SyllabusView.as_view(), name='Syllabus'),

        path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('create-course/', create_course, name='create-course'),
                    path('update_course/<int:course_id>/', views.update_course, name='update_course'),
        path('get_course/<int:course_id>/', views.get_course, name='get_course'),
    path('courses/', CourseView.as_view(), name='list_courses_with_sections'),
path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('Livemeeting/', LivemeetingView.as_view(), name='Livemeeting'),
    path('Lessons/', LessonView.as_view(), name='Lessons'),
    path('Livemeeting/<int:pk>/', LivemeetingDetailView.as_view(), name='Livemeeting-details'),
 path('Homeworks/', HomeworkView.as_view(), name='Homeworks'),
    path('ExamResult/', ExamResultView.as_view(), name='ExamResult'),
        path('Syllabus/<int:pk>/', SyllabusStudentDetailView.as_view(), name='Syllabus-details'),
 path('OnlineExam/', OnlineExamView.as_view(), name='OnlineExam'),
  path('LessonPlan/', LessonPlanView.as_view(), name='LessonPlan'),
    path('Subjects/', SubjectView.as_view(), name='Subjects'),
        path('OnlineExam/<int:pk>/',OnlineExamDetailView.as_view(), name='OnlineExam-details'),
    path('ExamResult/<int:pk>/', ExamResultDetailView.as_view(), name='ExamResult-details'),
    path('SubmitedHomworks/', SubmitedHomworksView.as_view(), name='SubmitedHomworks'),
        path('api/home-data/', views.home_data, name='home_data'),
    path('', include(router.urls)),
    path('', include(course_sections_router.urls)),
    path('', include(video_lessons_router.urls)),
    path('', include(quizzes_router.urls)),
    path('', include(questions_router.urls)),
    # path('',views.index,name='index')
]

