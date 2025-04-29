from rest_framework import serializers
from .models import Vehicle, InspectionReport

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class InspectionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionReport
        fields = '__all__'
