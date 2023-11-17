from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..views import Drones

class ValidatorTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = Drones.as_view()

    def test_get_available_drones(self):
        request = self.factory.post('/available_drones')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_get_drone_by_key(self):
        request = self.factory.post('/available_drones/WERD53')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)