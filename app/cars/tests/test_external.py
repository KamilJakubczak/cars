from cars.datasources import VpicDatasource, VpicCar

from django.test import TestCase


class VpicTests(TestCase):

    def test_url_creation(self):
        v = VpicDatasource()
        v._get_models_url('honda')
        expected_url ='https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/honda?format=json'
        self.assertEqual(v.make_url, expected_url)


class VpicCarTests(TestCase):

    def test_check_model_in_make(self):
        v_datasource = VpicDatasource()
        car = VpicCar('honda', v_datasource)
        has_model = car.has_model('civic')
        not_have_model = car.has_model('passat')
        self.assertTrue(has_model)
        self.assertFalse(not_have_model)
