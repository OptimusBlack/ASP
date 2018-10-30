from django.db import models


class Stock(models.Model):
    def __str__(self):
        return self.name

    def get_full_stock(self):
        return self.objects.all()

    name = models.CharField(max_length=200)
    description = models.TextField(default="")
