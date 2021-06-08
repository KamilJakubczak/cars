import mock
import json
from cars import models
from .test_base import TestBase, EXTERNAL_RESPONSE_FIAT, POPULAR_URL


class TestPopular(TestBase):

    @mock.patch('requests.get')
    def test_get_popular_list(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(
            EXTERNAL_RESPONSE_FIAT)

        car = models.Car.objects.create(**self.CAR_1)
        car2 = models.Car.objects.create(**self.CAR_2)

        models.Rate.objects.create(car_id=car2, rate=4)
        models.Rate.objects.create(car_id=car, rate=4)
        models.Rate.objects.create(car_id=car, rate=4)

        res = self.client.get(POPULAR_URL)

        self.assertEqual(res.data[0]['rates_number'], 2)
