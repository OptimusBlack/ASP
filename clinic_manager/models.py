from django.db import models
from django.utils import timezone
import json
import uuid


class Order(models.Model):
    def __str__(self):
        return str(self.orderId)

    def createOrder(self, contents):
        self.dateOrdered = timezone.now()
        try:
            self.contents = json.dumps(contents)
        except json.JSONDecodeError:
            print("Error decoding JSON")

    def getOrderDetails(self, i):
        try:
            return self.objects.all()[i]
        except IndexError:
            print("The entry doesnot exist")
            return None

    orderId = models.UUIDField(default=uuid.uuid4, editable=False)
    dateOrdered = models.DateTimeField('Date of Order')
    contents = models.TextField(default="{}")
    orderStatus = models.TextField()
