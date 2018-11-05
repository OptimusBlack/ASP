from django.db import models
from home.models import User
from clinic_manager.models import Order


class Dispatcher(User):

    def __str__(self):
        return str(self.username)


class DispatchQueue(models.Model):
    """
    Model for the dispatch queue
    """
    def __str__(self):
        return str(self.queue_number)

    queue_number = models.IntegerField(default=-1)
    orders = [Order]

