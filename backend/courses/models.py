from django.db import models
from django.conf import settings  # <-- Correct way

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_courses')
    link = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)
    is_completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)
