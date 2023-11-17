from django.urls import path
from .views import *

urlpatterns = [
    path('',Drones.as_view(),name='view_available_drones'),
    path('register_drone',Drones.as_view(),name='register_drone'),
    path('load_medication/<str:serial_number>', MedicationView.as_view(),name='load_medication'),
    path('check_medication/<str:serial_number>', MedicationView.as_view(),name='check_loaded_medication'),
    path('available_drones', Drones.as_view(),name='available_drones'),
    path('drone_battery_level/<str:serial_number>', Drones.as_view(),name='drone_battery_level')
]