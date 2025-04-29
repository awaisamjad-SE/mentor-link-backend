# courses/serializers.py
from rest_framework import serializers
from .models import Course, Enrollment

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'progress', 'is_completed', 'last_accessed']
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'link']  # <-- include link
