from django.db import models
from django.utils import timezone
from home.models import User
import json


class ClinicManager(User):
    """
    User model for the user.

    Inherits the User model for common attributes
    """
    def __str__(self):
        """
        Display when printed
        :return: Username of the user in string format
        """
        return str(self.user.username)

    clinic_name = models.TextField(default='')


class Order(models.Model):
    """
    Model for an Order

    Represents an object of the order itself.
    """
    def __str__(self):
        return str(self.id)

    def create_order(self, clinic):
        print("Creating order....")
        self.date_ordered = timezone.now()
        self.order_status = 'Queued for Processing'
        self.order_clinic = clinic
        self.save()

    def get_order_by_index(self, i):
        try:
            return self.objects.all()[i]
        except IndexError:
            print("The entry does not exist")
            return None

    date_ordered = models.DateTimeField()
    contents = models.TextField(default=json.dumps({'contents': []}))
    total_weight = models.FloatField(default=0.0)
    priority_level = models.CharField(max_length=200, default='Low')
    order_status = models.TextField()
    order_clinic = models.TextField(default='')
    time_delivered = models.DateTimeField(blank=True, null=True)
    time_dispatched = models.DateTimeField(blank=True, null=True)
