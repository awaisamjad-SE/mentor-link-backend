# courses/urls.py
from django.urls import path
from .views import (
    ActiveCoursesView, CompletedCoursesView, UnwatchedCoursesView,
    TeacherCoursesView, StudentProgressView,
    EnrollCourseView, WatchCourseView,UploadCourseView,ListAllCoursesView
)

urlpatterns = [
    path('student/active-courses/', ActiveCoursesView.as_view()),
    path('student/completed-courses/', CompletedCoursesView.as_view()),
    path('student/unwatched-courses/', UnwatchedCoursesView.as_view()),
    path('teacher/courses/', TeacherCoursesView.as_view()),
    path('teacher/student-progress/', StudentProgressView.as_view()),
    path('courses/enroll/<int:course_id>/', EnrollCourseView.as_view()),
    path('courses/watch/<int:course_id>/', WatchCourseView.as_view()),
    path('teacher/upload-course/', UploadCourseView.as_view()),
    path('courses1/all/', ListAllCoursesView.as_view()),
]
