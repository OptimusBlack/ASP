from django.contrib import admin
from .models import DispatchQueue, Dispatcher

admin.site.register(DispatchQueue)
admin.site.register(Dispatcher)