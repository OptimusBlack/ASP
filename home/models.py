from django.db import models
from django.contrib.auth.models import User as UserDjango


class User(models.Model):
    """
    Model for a user in the application
    """
    user = models.OneToOneField(UserDjango, on_delete=models.CASCADE, default=None)


class RegistrationToken(models.Model):
    email = models.CharField(max_length=500)
    token = models.CharField(max_length=200)
    role = models.CharField(max_length=200)

