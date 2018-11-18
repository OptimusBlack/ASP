from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name="login"),
    path('register/', views.register, name='register'),
    path('register_token/', views.register_with_token, name='register_token')
]