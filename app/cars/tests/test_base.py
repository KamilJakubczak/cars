from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

CARS_URL = reverse('api:cars-list')
POPULAR_URL = reverse('api:popular-list')
RATE_URL = reverse('api:rate-list')


def get_car_details_url(pk):
    return reverse('api:cars-detail', args=[pk])


EXTERNAL_RESPONSE_FIAT = '''{"Count":10,"Message":
"Response returned successfully","SearchCriteria":"Make:fiat","Results":
[{"Make_ID":492,"Make_Name":"FIAT","Model_ID":2037,"Model_Name":"500L"},
{"Make_ID":492,"Make_Name":"FIAT","Model_ID":2055,"Model_Name":"500"},
{"Make_ID":492,"Make_Name":"FIAT","Model_ID":3490,"Model_Name":"Freemont"},
{"Make_ID":492,"Make_Name":"FIAT","Model_ID":10396,"Model_Name":"500X"},
{"Make_ID":492,"Make_Name":"FIAT","Model_ID":11448,"Model_Name":"124 Spider"},
{"Make_ID":492,"Make_Name":"FIAT","Model_ID":14603,"Model_Name":"Spider 2000"},
{"Make_ID":492,"Make_Name":"FIAT","Model_ID":14604,"Model_Name":"X 1\/9"},
{"Make_ID":492,"Make_Name":"FIAT","Model_ID":14605,"Model_Name":"Brava"},
{"Make_ID":492,"Make_Name":"FIAT","Model_ID":14606,"Model_Name":"Strada"},
{"Make_ID":492,"Make_Name":"FIAT","Model_ID":25128,"Model_Name":"Ducato"}]}'''

EXTERNAL_RESPONSE_OPEL = '''{"Count":7,"Message":
"Response returned successfully","SearchCriteria":"Make:opel","Results":
[{"Make_ID":471,"Make_Name":"OPEL","Model_ID":1840,"Model_Name":"Ampera"},
{"Make_ID":471,"Make_Name":"OPEL","Model_ID":4784,"Model_Name":"Roadster"},
{"Make_ID":471,"Make_Name":"OPEL","Model_ID":8719,"Model_Name":"Opel"},
{"Make_ID":471,"Make_Name":"OPEL","Model_ID":11486,"Model_Name":"Sintra"},
{"Make_ID":471,"Make_Name":"OPEL","Model_ID":13975,"Model_Name":"Ampera-e"},
{"Make_ID":471,"Make_Name":"OPEL","Model_ID":18979,"Model_Name":"Ampera-e EV"},
{"Make_ID":10922,"Make_Name":"PROPEL ","Model_ID":28596,"Model_Name":"PROPEL "}
]}'''
EXTERNAL_MODELS_FOR_FIAT = [
    '500L', '500', 'Freemont', '500X', '124 Spider',
    'Spider 2000', 'X 1/9', 'Brava', 'Strada', 'Ducato']


class TestBase(TestCase):

    def setUp(self):
        self.client = APIClient()

    CAR_1 = {
        'make': 'Fiat',
        'model': '500'
    }

    CAR_1_lower = {
        'make': 'fiat',
        'model': '500'
    }

    CAR_2 = {
        'make': 'Fiat',
        'model': 'Freemont'
    }
