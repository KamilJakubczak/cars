import json
from .test_base import TestBase
from cars.errors import CarApiErrors
from cars.error_handler import error_handler
from rest_framework.exceptions import ValidationError


class TestErrorHandler(TestBase):
    def test_invalid_api_usage(self):
        error = CarApiErrors.ExternalApiCarNotFound()
        res = error_handler(error, None)
        message = json.loads(res.content)['message']
        self.assertEqual(
            res.status_code, CarApiErrors.ExternalApiCarNotFound.code)
        self.assertEqual(
            message, CarApiErrors.ExternalApiCarNotFound.message)

    def test_validation_error(self):
        error = ValidationError({'field': ['Test message']})
        res = error_handler(error, None)
        message = json.loads(res.content)['message']
        self.assertEqual(
            res.status_code, 400)
        self.assertEqual(
            message, 'Test message')
