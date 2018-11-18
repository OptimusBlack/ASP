from django.db import models


class ProcessQueue(models.Model):
    def __str__(self):
        return str(self.order_id)

    order_id = models.IntegerField(default=-1)
    queue_no = models.IntegerField(default=-1)
