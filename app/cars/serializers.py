from rest_framework import serializers
from .models import Car, Rate
from django.db.models import Sum
from rest_framework.validators import ValidationError


class CarSerializer(serializers.ModelSerializer):
    avg_rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'avg_rate']

    def validate(self, car):
        self.duplicate_validation(car)
        return car

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
            raise ValidationError('Not unique. Provided car already exists.')
