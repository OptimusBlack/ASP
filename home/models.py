from django.db import models


class User(models.Model):
    """
    Model for a user in the application
    """
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_id = models.CharField(max_length=500)
    password = models.CharField(max_length=500)
