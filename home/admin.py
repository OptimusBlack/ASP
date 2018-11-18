from django.contrib import admin
from .models import RegistrationToken, User


admin.site.register(RegistrationToken)
admin.site.register(User)