from django.db import models


class Item(models.Model):
    """
    Model for the Product Catalog

    Object created represents a product in the catalog
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    weight_per_unit = models.FloatField()
    description = models.TextField(default='')
    category = models.CharField(max_length=200)


class LocationData(models.Model):
    name = models.TextField(default='')
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    alt = models.FloatField(default=0.0)
    distances = models.TextField(default='{}')
