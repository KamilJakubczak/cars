from rest_framework import viewsets, mixins
from django.db.models import Count
from .models import Car, Rate
from .serializers import CarSerializer, PopularSerializer, RateSerializer


class CarViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin, mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class PopularViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.annotate(
        count=Count('rate__car_id')).order_by('-count')
    serializer_class = PopularSerializer


class RateViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
