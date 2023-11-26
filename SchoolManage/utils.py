from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from django.shortcuts import get_object_or_404
def create_course_with_sections_quizzes_lessons(data):
    # Create the course first
    course_serializer = CourseSerializer(data=data)
    assign_teacher_pk = data.pop('assign_teacher')
    course_category_pk = data.pop('course_category')

    # Get the Teacher and CourseCategory instances
    assign_teacher = get_object_or_404(Teacher, pk=assign_teacher_pk)
    course_category = get_object_or_404(CourseCategory, pk=course_category_pk)

    # Create the course with the remaining data
    course_serializer = CourseSerializer(data=data)
    if course_serializer.is_valid():
        course = course_serializer.save()

        sections_data = data.get('sections', [])
        for section_data in sections_data:
            section_serializer = CourseSectionSerializer(data=section_data)
            if section_serializer.is_valid():
                section = section_serializer.save(course=course)
                lessons_data = section_data.get('lessons', [])
                for lesson_data in lessons_data:
                    lesson_serializer = LessonSerializer(data=lesson_data)
                    if lesson_serializer.is_valid():
                        lesson_serializer.save(section=section)

                quiz_data = section_data.get('quizzes', {})
                if quiz_data:
                    quiz_serializer = QuizSerializer(data=quiz_data)
                    if quiz_serializer.is_valid():
                        quiz = quiz_serializer.save(course=course, section=section)
                        questions_data = quiz_data.get('questions', [])
                        for question_data in questions_data:
                            question_serializer = QuestionSerializer(data=question_data)
                            if question_serializer.is_valid():
                                question = question_serializer.save(quiz=quiz)
                                choices_data = question_data.get('choices', [])
                                for choice_data in choices_data:
                                    ChoiceSerializer(data=choice_data).save(question=question)
                    else:
                        return Response(quiz_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Course, sections, quizzes, and lessons created successfully'}, status=status.HTTP_201_CREATED)




