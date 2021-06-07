from rest_framework import serializers
from .models import Car, Rate
from django.db.models import Sum
from .errors import CarApiErrors
from cars.datasources import VpicDatasource, VpicCar


class CarSerializer(serializers.ModelSerializer):
    avg_rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'avg_rate']

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
    def get_avg_rate(car):
        rate = Rate.objects.filter(car_id=car.id).aggregate(Sum('rate'))[
            'rate__sum']
        count = Rate.objects.filter(car_id=car.id).count()
        try:
            avg_rate = rate / count
        except TypeError:
            avg_rate = None
        return avg_rate

    @staticmethod
    def duplicate_validation(car):
        exists = Car.objects.filter(make__iexact=car['make'],
                                    model__iexact=car['model'])
        if exists:
            raise CarApiErrors.CarNotUnique
