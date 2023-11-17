from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..views import Drones
import json


class ValidatorTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = Drones.as_view()

    def test_get_available_drones(self):
        request = self.factory.get('/available_droneses')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_get_drone_by_key(self):
        request = self.factory.get('/available_drones/WERD53')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)


    def test_add_new_drone(self):
        data = {
        "serial_number": "testDrone",
        "model": "lightweight",
        "weight": 140,
        "battery_capacity": 21,
        "state": "idle"
        }
        request = self.factory.post('/register_drone',data)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_add_new_drone_bad_data(self):
        data = {
        "baddata": "test",
        }
        request = self.factory.post('/register_drone',data)
        response = self.view(request)
        response_content_str = response.content.decode('utf-8')
        response_data = json.loads(response_content_str)
        self.assertEqual(response_data['status'], 400)