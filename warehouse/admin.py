from django.contrib import admin
from .models import ProcessQueue, WarehousePersonnel


admin.site.register(ProcessQueue)
admin.site.register(WarehousePersonnel)