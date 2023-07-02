from django.http import JsonResponse
from .models import Drone, Medication
from .serializers import DroneSerializer, MedicationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

import re
from datetime import datetime


battery_tracking = []

@api_view(['POST'])
def register_drone(request):
    """Add a new drone object to the database
    Args:
        request (object): object containing data from a post request
    Returns:
        JsonResponse: An HTTP response class that consumes data,serializes
        to JSON, and JSON data is returned
    """
    if request.method == 'POST':
        serializer = DroneSerializer(data=request.data)
        if serializer.is_valid() and len(Drone.objects.all()) < 10:
            if serializer.validated_data['weight'] > 500:
                return JsonResponse({"status":"ERROR","message":"Drone above maximum weight limit (500gr)"})
            if serializer.validated_data['battery_capacity'] < 25:
                serializer.validated_data['state'] = 'idle'
            create_history_log(serializer.validated_data['serial_number'],serializer.validated_data['battery_capacity'])
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"status":"ERROR","message":"method not allowed"})


@api_view(['POST'])
def load_medication_on_drone(request,serial_number):
    """gets a drone using its serial number and loads the medication on it after all validations pass
    Args:
        request (object): object containing data from a post request
        serial_number (string): used as an identifier for a specific
    Returns:
        JsonResponse: An HTTP response class that consumes data,serializes
        to JSON, and JSON data is returned
    """
    try:
        drone = Drone.objects.get(serial_number=serial_number)
        medication = Medication.objects.filter(serial_number=serial_number)
        current_weight = 0
        create_history_log(drone.serial_number,drone.battery_capacity)
        for med in medication:
            current_weight+=med.weight

        medication_serializer = MedicationSerializer(data=request.data)
        if medication_serializer.is_valid():
            if validate_name(medication_serializer.validated_data['name']) and validate_code(medication_serializer.validated_data['code']):
                if is_validate_weight(drone.weight,medication_serializer.validated_data['weight'],current_weight):
                    if drone.battery_capacity > 25:
                        drone.state = 'loaded'
                        drone.save()
                        medication_serializer.save()
                        return JsonResponse({"medication":medication_serializer.validated_data},safe=False)
                    return JsonResponse({"message":f"battery for drone {drone.serial_number} is too low for loading"})
                return JsonResponse({"message":"medication too heavy"})
            return JsonResponse({"message":"name and code is not valid"})
        return JsonResponse({"message":"Invalid data passed"}, status=status.HTTP_400_BAD_REQUEST,safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"message":f"Drone {serial_number} does not exist"},status=status.HTTP_404_NOT_FOUND)

    
@api_view(['GET'])
def check_loaded_medication(request,serial_number):
    """Check the medication currently loaded on a drone using the serial number as a reference
    Args:
        request (object): object containing data from a get request
        serial_number (string): drone serial number to get the right medication loaded
    Returns:
        JsonResponse: An HTTP response class that consumes data,serializes
        to JSON, and JSON data is returned
    """
    if request.method == 'GET':
        medication = Medication.objects.filter(serial_number=serial_number)
        serializer = MedicationSerializer(medication,many=True)
        drone = Drone.objects.get(serial_number=serial_number)
        create_history_log(drone.serial_number,drone.battery_capacity)
        return JsonResponse({"drone":serial_number,"medication":serializer.data},safe=False)
    return JsonResponse({"status":"ERROR","message":"method not allowed"})
    

@api_view(['GET'])
def check_available_drones(request):
    """check if there are any drones whose status is idle which makes them available
    Args:
        request (object): object containing data from a post request
    Returns:
        JsonResponse: An HTTP response class that consumes data,serializes
        to JSON, and JSON data is returned
    """
    if request.method == 'GET':
        drones = Drone.objects.filter(state='idle')
        serializer = DroneSerializer(drones,many=True)
        return JsonResponse({"drones":serializer.data})
    return JsonResponse({"status":"ERROR","message":"method not allowed"})


@api_view(['GET'])
def check_drone_battery_level(request,serial_number):
    """get request to check to current battery level of the drone
    Args:
        request (object): get request object
        serial_number (string): number to identify a specific drone
    Returns:
        JsonResponse: An HTTP response class that consumes data,serializes
        to JSON, and JSON data is returned
    """
    if request.method == 'GET':
        try:
            drone = get_object_or_404(Drone,serial_number=serial_number)
            create_history_log(drone.serial_number,drone.battery_capacity)
            return JsonResponse({"battery_level":drone.battery_capacity,"log":battery_tracking})
        except ObjectDoesNotExist:
            return JsonResponse({"message":"Drone does not exist"},status=status.HTTP_404_NOT_FOUND)
    return JsonResponse({"status":"ERROR","message":"method not allowed"})
    

def validate_name(name):
    """validates if name only allows letters, numbers, dashes and underscores);
    Args:
        name (string): medication name
    Returns:
        boolean: returns true if the name matches the regular expression
                 and false if not
    """
    return re.match('^[a-zA-Z0-9_-]+$',name)


def validate_code(code):
    """validates if code only allows upper case letters, underscore and numbers
    Args:
        code (string): medication code
    Returns:
        boolean: returns true if the code matches the regular expression
                 and false if not
    """
    return re.match('^[A-Z0-9_]+$',code)

def is_validate_weight(drone_weight,medication_weight,current_weight):
    """validates if the new load being added does 
        not exceed the maximum weight specified for the robot
    Args:
        drone_weight (int): the specified drone weight limit
        medication_weight (int): the weight of the new madication to be loaded
        current_weight (int): the weight of the medication currently loaded on the drone
    Returns:
        boolean: returns true if the drone weight is higher than or equals the current
                 loaded medication weight added together with the new load weight
    """
    try:
        if int(drone_weight)>=(int(medication_weight)+current_weight):
            return True
    except ValueError:
        return None
    return False

def create_history_log(serial_number,battery_level):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    battery_tracking.append((serial_number,timestamp,battery_level))