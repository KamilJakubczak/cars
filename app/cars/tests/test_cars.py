import mock
import requests
import json
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from cars import models
from cars.errors import CarApiErrors, RateApiErrors

from cars.datasources import VpicCar, VpicDatasource

CARS_URL = reverse('api:cars-list')
POPULAR_URL = reverse('api:popular-list')
RATE_URL = reverse('api:rate-list')


def get_car_details_url(pk):
    return reverse('api:cars-detail', args=[pk])


EXTERNAL_RESPONSE_FIAT = '{"Count":10,"Message":"Response returned successfully","SearchCriteria":"Make:fiat","Results":[{"Make_ID":492,"Make_Name":"FIAT","Model_ID":2037,"Model_Name":"500L"},{"Make_ID":492,"Make_Name":"FIAT","Model_ID":2055,"Model_Name":"500"},{"Make_ID":492,"Make_Name":"FIAT","Model_ID":3490,"Model_Name":"Freemont"},{"Make_ID":492,"Make_Name":"FIAT","Model_ID":10396,"Model_Name":"500X"},{"Make_ID":492,"Make_Name":"FIAT","Model_ID":11448,"Model_Name":"124 Spider"},{"Make_ID":492,"Make_Name":"FIAT","Model_ID":14603,"Model_Name":"Spider 2000"},{"Make_ID":492,"Make_Name":"FIAT","Model_ID":14604,"Model_Name":"X 1\/9"},{"Make_ID":492,"Make_Name":"FIAT","Model_ID":14605,"Model_Name":"Brava"},{"Make_ID":492,"Make_Name":"FIAT","Model_ID":14606,"Model_Name":"Strada"},{"Make_ID":492,"Make_Name":"FIAT","Model_ID":25128,"Model_Name":"Ducato"}]}'
EXTERNAL_RESPONSE_OPEL = '{"Count":7,"Message":"Response returned successfully","SearchCriteria":"Make:opel","Results":[{"Make_ID":471,"Make_Name":"OPEL","Model_ID":1840,"Model_Name":"Ampera"},{"Make_ID":471,"Make_Name":"OPEL","Model_ID":4784,"Model_Name":"Roadster"},{"Make_ID":471,"Make_Name":"OPEL","Model_ID":8719,"Model_Name":"Opel"},{"Make_ID":471,"Make_Name":"OPEL","Model_ID":11486,"Model_Name":"Sintra"},{"Make_ID":471,"Make_Name":"OPEL","Model_ID":13975,"Model_Name":"Ampera-e"},{"Make_ID":471,"Make_Name":"OPEL","Model_ID":18979,"Model_Name":"Ampera-e EV"},{"Make_ID":10922,"Make_Name":"PROPEL ","Model_ID":28596,"Model_Name":"PROPEL "}]}'


class CarsTests(TestCase):
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

    def setUp(self):
        self.client = APIClient()

    @mock.patch('requests.get')
    def test_create_car_successful(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(EXTERNAL_RESPONSE_FIAT)
        res = self.client.post(CARS_URL, self.CAR_1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    @mock.patch('requests.get')
    def test_create_car_non_existing_car_external(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(EXTERNAL_RESPONSE_OPEL)
        res = self.client.post(CARS_URL, self.CAR_1)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            CarApiErrors.ExternalApiCarNotFound.message,
            res.json()['message'])

    @mock.patch('requests.get')
    def test_create_car_duplication_error(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(EXTERNAL_RESPONSE_FIAT)
        self.client.post(CARS_URL, self.CAR_1)
        res2 = self.client.post(CARS_URL, self.CAR_1)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            CarApiErrors.CarNotUnique.message,
            res2.json()['message'])

    @mock.patch('requests.get')
    def test_create_car_duplication_case_insensitive_error(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(EXTERNAL_RESPONSE_FIAT)
        self.client.post(CARS_URL, self.CAR_1)
        res2 = self.client.post(CARS_URL, self.CAR_1_lower)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            CarApiErrors.CarNotUnique.message,
            res2.json()['message'])

    @mock.patch('requests.get')
    def test_create_multiple_cars(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(EXTERNAL_RESPONSE_FIAT)
        self.client.post(CARS_URL, self.CAR_1)
        self.client.post(CARS_URL, self.CAR_2)
        cars = models.Car.objects.all()
        self.assertEqual(len(cars), 2)

    def test_delete_existing(self):
        car = models.Car.objects.create(**self.CAR_1)
        details_url = get_car_details_url(car.id)
        self.client.delete(details_url)
        car_after_delete = models.Car.objects.filter(pk=car.id)
        self.assertEqual(len(car_after_delete), 0)

    def test_delete_non_existing(self):
        details_url = get_car_details_url(-99)
        res = self.client.delete(details_url)

        self.assertEqual(res.status_code, 404)
        self.assertEqual('Not found.', res.json()['message'])

    def test_get_single_existing(self):
        car = models.Car.objects.create(**self.CAR_1)
        details_url = get_car_details_url(car.id)
        res = self.client.get(details_url)
        self.assertEqual(res.status_code, 200)

    def test_get_single_non_existing(self):
        details_url = get_car_details_url(-99)
        res = self.client.get(details_url)
        self.assertEqual(res.status_code, 404)

    def test_put_not_allowed(self):
        car = models.Car.objects.create(**self.CAR_1)
        details_url = get_car_details_url(car.id)
        res = self.client.put(details_url, {'make': 'make', 'model': 'model'})
        self.assertEqual(res.status_code, 405)

    # POPULAR
    @mock.patch('requests.get')
    def test_get_popular_list(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(EXTERNAL_RESPONSE_FIAT)
        car = models.Car.objects.create(**self.CAR_1)
        car2 = models.Car.objects.create(**self.CAR_2)

        models.Rate.objects.create(car_id=car2, rate=4)
        models.Rate.objects.create(car_id=car, rate=4)
        models.Rate.objects.create(car_id=car, rate=4)

        res = self.client.get(POPULAR_URL)

        self.assertEqual(res.data[0]['rates_number'], 2)

    # RATES
    def test_add_rate_success(self):
        car = models.Car.objects.create(**self.CAR_1)
        rate = self.client.post(RATE_URL, {'car_id': car.id, 'rate': 3})
        r = models.Rate.objects.filter(pk=rate.data['id'])[0]
        self.assertEqual(rate.data['id'], r.id)

    def test_add_rate_fail(self):
        rate = self.client.post(RATE_URL, {'car_id': 1, 'rate': 3})
        self.assertEqual(rate.status_code, 400)

    def test_add_rate_fail_min(self):
        car = models.Car.objects.create(**self.CAR_1)
        rate = self.client.post(RATE_URL, {'car_id': car.id, 'rate': 0})
        self.assertEqual(rate.status_code, 400)
        self.assertEqual(
            RateApiErrors.InvalidRateMin.message,
           rate.json()['message'])

    def test_add_rate_fail_max(self):
        car = models.Car.objects.create(**self.CAR_1)
        rate = self.client.post(RATE_URL, {'car_id': car.id, 'rate': 6})
        self.assertEqual(rate.status_code, 400)
        self.assertEqual(
            RateApiErrors.InvalidRateMax.message,
           rate.json()['message'])
