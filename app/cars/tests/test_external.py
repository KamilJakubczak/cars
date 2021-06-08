import mock
import json
from .test_base import TestBase, EXTERNAL_RESPONSE_FIAT, \
    EXTERNAL_MODELS_FOR_FIAT
from cars.datasources import VpicDatasource, VpicCar


class TestVpicDatabase(TestBase):

    def test_url_creation(self):
        v = VpicDatasource()
        v._get_models_url('honda')
        expected_url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/honda?format=json'
        self.assertEqual(v.make_url, expected_url)


class TestVpicCar(TestBase):

    @mock.patch('requests.get')
    def test_get_models(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(
            EXTERNAL_RESPONSE_FIAT)
        vpic_datasource = VpicDatasource()
        models = vpic_datasource.get_models_for_make('Fiat')
        self.assertEqual(models, EXTERNAL_MODELS_FOR_FIAT)

    @mock.patch('requests.get')
    def test_has_model(self, mocked_fn):
        mocked_fn.return_value = mock.Mock()
        mocked_fn.return_value.json.return_value = json.loads(
            EXTERNAL_RESPONSE_FIAT)
        vpic_datasource = VpicDatasource()
        vpic = VpicCar('Fiat', vpic_datasource)
        self.assertTrue(vpic.has_model('500'))
        self.assertFalse(vpic.has_model('Passat'))
