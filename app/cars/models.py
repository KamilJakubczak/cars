from django.db import models


class Car(models.Model):
    class Meta:
        unique_together = ['make', 'model']

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.make} {self.model}'


class Rate(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField()
