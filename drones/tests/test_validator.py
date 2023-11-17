from django.test import TestCase

import unittest
from datetime import datetime
from ..validator import Validator


class ValidatorTests(TestCase):
    def setUp(self):
        self.validator = Validator()

    def test_validate_name_valid(self):
        result = self.validator.validate_name("valid_Name123")
        self.assertTrue(result)

    def test_validate_name_invalid(self):
        result = self.validator.validate_name("invalid@Name")
        self.assertFalse(result)

    def test_validate_code_valid(self):
        result = self.validator.validate_code("VALID_CODE_123")
        self.assertTrue(result)

    def test_validate_code_invalid(self):
        result = self.validator.validate_code("invalid Code")
        self.assertFalse(result)

    def test_is_validate_weight_valid(self):
        result = self.validator.is_validate_weight(100, 20, 50)
        self.assertTrue(result)

    def test_is_validate_weight_invalid(self):
        result = self.validator.is_validate_weight(100, 60, 50)
        self.assertFalse(result)

    def test_is_validate_weight_non_integer_values(self):
        result = self.validator.is_validate_weight("100", "20", "y")
        self.assertIsNone(result)

    def test_is_validate_weight_string_integer_values(self):
        result = self.validator.is_validate_weight("100", "20", "20")
        self.assertTrue(result)

    # def test_create_history_log(self):
    #     serial_number = "123"
    #     battery_level = 80
    #     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     self.validator.create_history_log(serial_number, battery_level)
    #     self.assertEqual(self.validator.battery_tracking, [(serial_number, timestamp, battery_level)])

if __name__ == '__main__':
    unittest.main()
