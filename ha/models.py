from django.db import models


class Stock(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
