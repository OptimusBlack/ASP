from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register, name='register'),
    path('register_token/', views.register_with_token, name='register_token'),
    path('register_after_token/', views.register_after_token, name='register_after_token')
]