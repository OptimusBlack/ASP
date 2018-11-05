from django.db import models


class Item(models.Model):
    """
    Model for the Product Catalog

    Object created represents a product in the catalog
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    weight_per_unit = models.FloatField(default=0.0)
    description = models.TextField(default='Amazing medicine')
    category = models.CharField(max_length=200, default='IV Fluids')


class LocationData(models.Model):
    name = models.TextField(default='{}')
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    alt = models.FloatField(default=0.0)
    distances = models.TextField(default='{}')
