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
        return str(self.username)

    # This needs to be handled using json.dumps() and json.loads()
    order_cart = models.TextField(default="{}")


class Order(models.Model):
    """
    Model for an Order

    Represents an object of the order itself.
    """
    def __str__(self):
        return str(self.id)

    def create_order(self):
        self.date_ordered = timezone.now()
        self.order_status = 'Queued for Processing'
        self.save()

    def  add_to_order(self, order):
        """
        Add a product to order
        :param order: {id, weight, qty}
        :return: None
        """
        order_id = order.id
        old_contents = list(json.loads(self.contents).orders)
        old_contents.append({'order_id': order_id, 'qty': order.qty})

        self.total_weight += order.weight * order.qty
        self.contents = json.dumps(old_contents)
        self.priority_level = order.priority

    def get_order_by_index(self, i):
        try:
            return self.objects.all()[i]
        except IndexError:
            print("The entry does not exist")
            return None

    date_ordered = models.DateTimeField('Date of Order')
    # This needs to be handled using json.dumps() and json.loads()
    contents = models.TextField(default="{}")
    total_weight = models.FloatField(default=0.0)
    priority_level = models.CharField(max_length=200, default='')
    order_status = models.TextField()
