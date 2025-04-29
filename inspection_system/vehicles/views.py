from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vehicle, InspectionReport
from .serializers import VehicleSerializer, InspectionReportSerializer

# ViewSet for Vehicle CRUD
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

# Check if a vehicle exists
@api_view(['GET'])
def check_vehicle(request, vehicle_id):
    exists = Vehicle.objects.filter(id=vehicle_id).exists()
    return Response({"exists": exists})

# Get inspection reports for a vehicle
@api_view(['GET'])
def get_inspection(request, vehicle_id, inspection_type):
    reports = InspectionReport.objects.filter(vehicle_id=vehicle_id, inspection_type=inspection_type)
    serializer = InspectionReportSerializer(reports, many=True)
    return Response({"reports": serializer.data})

# Save inspection report
@api_view(['POST'])
def save_inspection(request):
    data = request.data
    vehicle_id = data.get("vehicle_id")
    inspection_type = data.get("inspection_type")
    parameters = data.get("parameters", [])

    # Check if vehicle exists
    if not Vehicle.objects.filter(id=vehicle_id).exists():
        return Response({"error": "Vehicle does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    # Delete existing inspection reports of this type for the vehicle
    InspectionReport.objects.filter(vehicle_id=vehicle_id, inspection_type=inspection_type).delete()

    # Save new parameters
    for param in parameters:
        InspectionReport.objects.create(
            vehicle_id=vehicle_id,
            inspection_type=inspection_type,
            parameter=param.get("parameter"),
            status=param.get("status"),
            observation=param.get("observation")
        )

    return Response({"message": "Inspection saved successfully"})
