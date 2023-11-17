from django.http import JsonResponse
from .models import Drone, Medication
from .serializers import DroneSerializer, MedicationSerializer
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .validator import Validator


class Drones(APIView,Validator):
    
    battery_capacity = 25
    max_weight = 500
    state = 'idle'
    max_drones = 10
    validator = Validator()

    def post(self,request):
        """Add a new drone object to the database
        Args:
            request (object): object containing data from a post request
        Returns:
            JsonResponse: An HTTP response class that consumes data,serializes
            to JSON, and JSON data is returned
        """
        serializer = DroneSerializer(data=request.data)
        if serializer.is_valid() and len(Drone.objects.all()) < self.max_drones:
            weight = serializer.validated_data.get('weight', 0)
            battery_capacity = serializer.validated_data.get('battery_capacity', 0)
            if weight > self.max_weight:
                return JsonResponse({"status":"ERROR","message":"Drone above maximum weight limit (500gr)"})
            if battery_capacity < self.battery_capacity:
                serializer.validated_data['state'] = 'idle'
            self.validator.create_history_log(serializer.validated_data['serial_number'],serializer.validated_data['battery_capacity'])
            serializer.save()
            return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"message":"data is not valid","status":status.HTTP_400_BAD_REQUEST})
        
    
    def get(self, request, serial_number=None):
        if serial_number:
            try:
                drone = get_object_or_404(Drone, serial_number=serial_number)
                self.validator.create_history_log(drone.serial_number, drone.battery_capacity)
                return JsonResponse({"battery_level": drone.battery_capacity, "log": "battery_tracking"})
            except ObjectDoesNotExist:
                return JsonResponse({"message": "Drone does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            all_drones = Drone.objects.filter(state='idle')
            serialized_drones = DroneSerializer(all_drones, many=True)
            return JsonResponse({'drones': serialized_drones.data})


class MedicationView(APIView,Validator):
    validator = Validator()

    def post(self, request, serial_number):
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
            self.validator.create_history_log(drone.serial_number, drone.battery_capacity)
            for med in medication:
                current_weight += med.weight
            medication_serializer = MedicationSerializer(data=request.data)
            if medication_serializer.is_valid():
                if (
                    self.validator.validate_name(medication_serializer.validated_data['name'])
                    and self.validator.validate_code(medication_serializer.validated_data['code'])
                ):
                    if self.validator.is_validate_weight(
                        drone.weight,
                        medication_serializer.validated_data['weight'],
                        current_weight,
                    ):
                        if drone.battery_capacity > 25:
                            drone.state = 'loaded'
                            drone.save()
                            medication_serializer.save()
                            return JsonResponse(
                                {"medication": medication_serializer.validated_data},
                                safe=False
                            )
                        return JsonResponse(
                            {"message": f"battery for drone {drone.serial_number} is too low for loading"}
                        )
                    return JsonResponse({"message": "medication too heavy"})
                return JsonResponse({"message": "name and code is not valid"})
            return JsonResponse(
                {"message": "Invalid data passed"},
                status=status.HTTP_400_BAD_REQUEST,
                safe=False,
            )
        except ObjectDoesNotExist:
            return JsonResponse(
                {"message": f"Drone {serial_number} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def get(self,request,serial_number):
        """Check the medication currently loaded on a drone using the serial number as a reference
        Args:
            request (object): object containing data from a get request
            serial_number (string): drone serial number to get the right medication loaded
        Returns:
            JsonResponse: An HTTP response class that consumes data,serializes
            to JSON, and JSON data is returned
        """
        medication = Medication.objects.filter(serial_number=serial_number)
        serializer = MedicationSerializer(medication,many=True)
        drone = Drone.objects.get(serial_number=serial_number)
        self.validator.create_history_log(drone.serial_number,drone.battery_capacity)
        return JsonResponse({"drone":serial_number,"medication":serializer.data},safe=False)


