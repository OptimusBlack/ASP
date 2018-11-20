from django.db import models
from home.models import User


class WarehousePersonnel(User):
    def __str__(self):
        """
        Display when printed
        :return: Username of the user in string format
        """
        return str(self.user.username)


class ProcessQueue(models.Model):
    def __str__(self):
        return str(self.order_id)

    order_id = models.IntegerField(default=-1)
    queue_no = models.IntegerField(default=-1)
