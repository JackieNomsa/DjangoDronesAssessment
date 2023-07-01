from django.http import JsonResponse
from .models import Drone, Medication
from .serializers import DroneSerializer, MedicationSerializer


def register_drone(request):

    pass

def load_medication_on_drone(request):
    pass

def check_loaded_medication(request,serial_number):
    pass

def check_available_drones(request):
    drones = Drone.objects.all()
    serializer = DroneSerializer(drones,many=True)
    return JsonResponse({"drones":serializer.data})

def check_drone_battery_level(request,serial_number):
    pass