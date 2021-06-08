from rest_framework import serializers
from django.db.models import Sum
from .errors import CarApiErrors, RateApiErrors
from .datasources import VpicDatasource, VpicCar
from .models import Car, Rate


class CarSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'avg_rating']

    def validate(self, car):
        self.duplicate_validation(car)
        self.external_check(car)
        return car

    def external_check(self, car):
        datasource = VpicDatasource()
        v_car = VpicCar(car['make'], datasource)
        if not v_car.has_model(car['model']):
            raise CarApiErrors.ExternalApiCarNotFound

    @staticmethod
    def get_avg_rating(car):
        rate = Rate.objects.filter(car_id=car.id).aggregate(Sum('rating'))[
            'rating__sum']
        count = Rate.objects.filter(car_id=car.id).count()
        try:
            avg_rating = round(rate / count, 1)
        except TypeError:
            avg_rating = None
        return avg_rating

    @staticmethod
    def duplicate_validation(car):
        exists = Car.objects.filter(make__iexact=car['make'],
                                    model__iexact=car['model'])
        if exists:
            raise CarApiErrors.CarNotUnique


class PopularSerializer(serializers.ModelSerializer):
    rates_number = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'rates_number']

    @staticmethod
    def get_rates_number(car):
        rates_number = Rate.objects.filter(car_id=car.id).count()
        return rates_number


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'car_id', 'rating']

    def validate(self, rate):
        self.rate_validation(rate['rating'])
        return rate

    @staticmethod
    def rate_validation(rate):
        if not isinstance(rate, int):
            raise RateApiErrors.InvalidRateType
        if rate < 1:
            raise RateApiErrors.InvalidRateMin
        if rate > 5:
            raise RateApiErrors.InvalidRateMax
