from django.db import models
from home.models import User
from clinic_manager.models import Order
import json


class Dispatcher(User):

    def __str__(self):
        return str(self.user.username)


class DispatchQueue(models.Model):
    """
    Model for the dispatch queue
    """
    def __str__(self):
        return str(self.queue_number)

    queue_number = models.IntegerField()
    order_id = models.IntegerField()
