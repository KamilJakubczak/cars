import mock
import json
from .test_base import TestBase, EXTERNAL_RESPONSE_OPEL, \
    EXTERNAL_RESPONSE_FIAT, CARS_URL, get_car_details_url
from rest_framework import status
from cars import models
from cars.errors import CarApiErrors


class CarsTests(TestBase):

    @mock.patch('requests.get')
    def test_create_car_successful(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(
            EXTERNAL_RESPONSE_FIAT)
        res = self.client.post(CARS_URL, self.CAR_1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    @mock.patch('requests.get')
    def test_create_car_non_existing_car_external(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(
            EXTERNAL_RESPONSE_OPEL)
        res = self.client.post(CARS_URL, self.CAR_1)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            CarApiErrors.ExternalApiCarNotFound.message,
            res.json()['message'])

    @mock.patch('requests.get')
    def test_create_car_duplication_error(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(
            EXTERNAL_RESPONSE_FIAT)
        self.client.post(CARS_URL, self.CAR_1)
        res2 = self.client.post(CARS_URL, self.CAR_1)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            CarApiErrors.CarNotUnique.message,
            res2.json()['message'])

    @mock.patch('requests.get')
    def test_create_car_duplication_case_insensitive_error(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(
            EXTERNAL_RESPONSE_FIAT)
        self.client.post(CARS_URL, self.CAR_1)
        res2 = self.client.post(CARS_URL, self.CAR_1_lower)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            CarApiErrors.CarNotUnique.message,
            res2.json()['message'])

    @mock.patch('requests.get')
    def test_create_multiple_cars(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(
            EXTERNAL_RESPONSE_FIAT)
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
        res = self.client.put(
            details_url, {'make': 'make', 'model': 'model'})
        self.assertEqual(res.status_code, 405)
