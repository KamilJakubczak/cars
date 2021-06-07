from rest_framework import viewsets, mixins
from .models import Car, Rate

from django.db.models import Count
from .serializers import CarSerializer, PopularSerializer


class CarViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin, mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class PopularViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.annotate(count=Count('rate__car_id')).order_by('-count')
    serializer_class = PopularSerializer
