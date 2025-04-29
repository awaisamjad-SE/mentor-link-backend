# courses/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer

# STUDENT APIs

class ActiveCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "Student":
            return Response({'detail': 'Only students can access this.'}, status=status.HTTP_403_FORBIDDEN)
        
        enrollments = Enrollment.objects.filter(student=request.user, is_completed=False, progress__gt=0)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

class CompletedCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "Student":
            return Response({'detail': 'Only students can access this.'}, status=status.HTTP_403_FORBIDDEN)
        
        enrollments = Enrollment.objects.filter(student=request.user, is_completed=True)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

class UnwatchedCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "Student":
            return Response({'detail': 'Only students can access this.'}, status=status.HTTP_403_FORBIDDEN)
        
        enrollments = Enrollment.objects.filter(student=request.user, progress=0)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

# TEACHER APIs

class TeacherCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "Teacher":
            return Response({'detail': 'Only teachers can access this.'}, status=status.HTTP_403_FORBIDDEN)
        
        courses = Course.objects.filter(teacher=request.user)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class StudentProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "Teacher":
            return Response({'detail': 'Only teachers can access this.'}, status=status.HTTP_403_FORBIDDEN)
        
        enrollments = Enrollment.objects.filter(course__teacher=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

# COMMON APIs

class EnrollCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        if request.user.role != "Student":
            return Response({'detail': 'Only students can enroll.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            course = Course.objects.get(id=course_id)
            enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
            if created:
                return Response({'message': 'Enrolled successfully!'})
            else:
                return Response({'message': 'Already enrolled!'})
        except Course.DoesNotExist:
            return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

class WatchCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        if request.user.role != "Student":
            return Response({'detail': 'Only students can watch courses.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            enrollment = Enrollment.objects.get(student=request.user, course_id=course_id)
            enrollment.progress += 10  # Increment by 10% on each call for demo
            if enrollment.progress >= 100:
                enrollment.progress = 100
                enrollment.is_completed = True
            enrollment.save()
            return Response({'message': 'Progress updated.', 'progress': enrollment.progress})
        except Enrollment.DoesNotExist:
            return Response({'error': 'Not enrolled in this course.'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Course
from .serializers import CourseSerializer

class UploadCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'Teacher':
            return Response({'error': 'Only teachers can upload courses.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=user)
            return Response({'message': 'Course uploaded successfully.', 'course': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Course
from .serializers import CourseSerializer

class ListAllCoursesView(APIView):
    permission_classes = [permissions.AllowAny]  # anyone can access

    def get(self, request):
        courses = Course.objects.all().order_by('-created_at')  # latest first
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
