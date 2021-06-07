import mock
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from cars import models
from cars.errors import CarApiErrors

from cars.datasources import VpicCar

CARS_URL = reverse('api:cars-list')


def get_car_details_url(pk):
    return reverse('api:cars-detail', args=[pk])


class CarsTests(TestCase):
    CAR_1 = {
        'make': 'Fiat',
        'model': 'Multipla'
    }

    CAR_1_lower = {
        'make': 'fiat',
        'model': 'multipla'
    }

    CAR_2 = {
        'make': 'Volkswagen',
        'model': 'Passat'
    }

    def setUp(self):
        self.client = APIClient()

# TODO doeck na test błędua
    @mock.patch('cars.datasources.external_api.VpicCar.has_model', return_value=True)
    def test_create_car_successful(self, mocked_fn):
        res = self.client.post(CARS_URL, self.CAR_1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    @mock.patch('cars.datasources.external_api.VpicCar.has_model', return_value=False)
    def test_create_car_non_existing_car_external(self, mocked_fn):
        res = self.client.post(CARS_URL, self.CAR_1)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            CarApiErrors.ExternalApiCarNotFound.message,
            res.json()['message'])

    @mock.patch('cars.datasources.external_api.VpicCar.has_model', return_value=True)
    def test_create_car_duplication_error(self, mocked_fn):
        self.client.post(CARS_URL, self.CAR_1)
        res2 = self.client.post(CARS_URL, self.CAR_1)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            CarApiErrors.CarNotUnique.message,
            res2.json()['message'])

    @mock.patch('cars.datasources.external_api.VpicCar.has_model', return_value=True)
    def test_create_car_duplication_case_insensitive_error(self, mocked_fn):
        self.client.post(CARS_URL, self.CAR_1)
        res2 = self.client.post(CARS_URL, self.CAR_1_lower)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            CarApiErrors.CarNotUnique.message,
            res2.json()['message'])

    @mock.patch('cars.datasources.external_api.VpicCar.has_model', return_value=True)
    def test_create_multiple_cars(self, mocked_fn):
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
