from django.db import models

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    pending_work = models.TextField()
    exit_status = models.BooleanField(default=False)

class InspectionReport(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    inspection_type = models.CharField(max_length=100)
    parameter = models.CharField(max_length=200)
    status = models.CharField(max_length=10)
    observation = models.TextField()
