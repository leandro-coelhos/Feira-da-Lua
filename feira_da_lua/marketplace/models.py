from django.db import models
from django.conf import settings

class MarketPlace(models.Model):
    name = models.CharField(max_length=255)
    marketer = models.ForeignKey("users.Marketer", blank=True, null=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.BinaryField()
    marketer = models.ForeignKey("users.Marketer", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    