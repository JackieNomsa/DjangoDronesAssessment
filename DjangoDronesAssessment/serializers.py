from rest_framework import serializers
from .models import Drone,Medication


class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ["serial_number","model","weight","battery_capacity","state"]


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ["name","weight","code","image"]