from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, check_vehicle, get_inspection, save_inspection

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('check_vehicle/<int:vehicle_id>/', check_vehicle),
    path('get_inspection/<int:vehicle_id>/<str:inspection_type>/', get_inspection),
    path('save_inspection/', save_inspection),
]
