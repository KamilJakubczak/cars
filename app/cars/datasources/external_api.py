import requests as r
from abc import ABC, abstractmethod
from dataclasses import dataclass


class CarDatasource(ABC):

    @abstractmethod
    def get_models_for_make(self, make: str) -> list:
        raise NotImplemented


class VpicDatasource(CarDatasource):
    URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/%s?format=json'

    def __init__(self):
        self._make = None
        self.model = None
        self.make_url = None
        self.response = None

    @property
    def make(self):
        return self._make

    def _get_models_url(self, make: str) -> None:
        self.make_url = self.URL % make

    def _get_external_response(self):
        self.response = r.get(self.make_url)

    def get_models_for_make(self, make: str) -> list:
        self._get_models_url(make)
        self._get_external_response()
        dict_data = self.response.json()
        return [row['Model_Name'] for row in dict_data['Results']]


class VpicCar:

    def __init__(self, make: str, datasource: CarDatasource):
        self._available_models = None
        self._make = make
        self._datasource = datasource
        self._get_available_models()

    @property
    def make(self):
        return self._make

    @property
    def models(self):
        return self._available_models

    def _get_available_models(self):
        self._available_modes = self._datasource.get_models_for_make(self._make)

    def has_model(self, model: str) -> bool:
        if model.lower() in [m.lower() for m in self._available_modes]:
            return True
        return False
