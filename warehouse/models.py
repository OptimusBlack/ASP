from django.db import models


class ProcessQueue(models.Model):
    def __str__(self):
        return self.order_id

    order_id = models.IntegerField,
    queue_no = models.IntegerField

