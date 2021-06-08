from cars import models
from .test_base import TestBase, RATE_URL
from cars.errors import RateApiErrors


class TestRate(TestBase):

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
