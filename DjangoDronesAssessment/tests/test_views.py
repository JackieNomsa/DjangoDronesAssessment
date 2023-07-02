from django.test import TestCase
from django.test import Client
from ..views import validate_name,validate_code,is_validate_weight
import base64

class ViewsTests(TestCase):
    client = Client()

    def test_register_drone_post_request(self):        
        response = self.client.post('/register_drone',
                                    {
            "serial_number": "46ER",
            "model": "heavyweight",
            "weight": 200,
            "battery_capacity": 69,
            "state": "idle"
        })
        self.assertEqual(201,response.status_code)

    def test_availble_drones_get_request(self):
        data = {
            "serial_number": "46ER",
            "model": "heavyweight",
            "weight": 200,
            "battery_capacity": 69,
            "state": "idle"
        }
        post_response = self.client.post('/register_drone',data=data)
        get_response = self.client.get('/available_drones')
        self.assertEqual(post_response.status_code,201)
        self.assertTrue(get_response.status_code,200)


    def test_load_medication(self):
        with open('/home/hela/Dev/4-sure/assessment/DjangoDronesAssessment/5891110.jpg', 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            data = {
            "serial_number": "46ER",
            "model": "heavyweight",
            "weight": 200,
            "battery_capacity": 69,
            "state": "idle"
        }
        post_response = self.client.post('/register_drone',data=data)
        data = {"name":"testing1",
                "weight":80,
                "code":"QWE7",
                "serial_number":"46ER",
                "image":encoded_image}
        response = self.client.post('/load_medication/46ER',data=data)
        print(response.content)
        self.assertEqual(post_response.status_code,201)
        self.assertEqual(201,response.status_code)

    def test_check_medication(self):
        data = {
            "serial_number": "46ER",
            "model": "heavyweight",
            "weight": 200,
            "battery_capacity": 69,
            "state": "idle"
        }
        post_response = self.client.post('/register_drone',data=data)
        get_response = self.client.get('/check_medication/46ER')
        self.assertTrue(get_response.status_code,200)

    def test_drone_battery(self):
        data = {
            "serial_number": "46ER",
            "model": "heavyweight",
            "weight": 200,
            "battery_capacity": 69,
            "state": "idle"
        }
        post_response = self.client.post('/register_drone',data=data)
        get_response = self.client.get('/drone_battery/46ER')
        self.assertTrue(get_response.status_code,200)

    def test_validate_name(self):
        result = validate_name('45@sd-_')
        self.assertFalse(result,'name is not a valid format')
        result = validate_name('RE45-_')
        self.assertTrue(result)

    def test_validate_code(self):
        result = validate_code('45@sd-_')
        self.assertFalse(result,'code is not a valid format')
        result = validate_code('RE-_')
        self.assertFalse(result,'code is not a valid format')
        result = validate_code('RE8_')
        self.assertTrue(result,'code is not a valid format')

    def test_is_valid_weight(self):
        result = is_validate_weight(200,300,0)
        self.assertFalse(result)
        result = is_validate_weight(200,90,250)
        self.assertFalse(result)
        result = is_validate_weight(200,90,0)
        self.assertTrue(result)
        result = is_validate_weight(200,90,100)
        self.assertTrue(result)

