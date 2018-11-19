from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('pop/', views.do_pop, name='pop'),
    path('process/', views.process, name='process'),
]
