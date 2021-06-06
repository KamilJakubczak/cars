from rest_framework import viewsets, mixins
from .models import Car
from .serializers import CarSerializer


class CarViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin, mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
