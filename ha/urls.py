from django.urls import path
from . import views

urlpatterns = [
    path('addstock/', views.add_stock, name='add_stock')
]
