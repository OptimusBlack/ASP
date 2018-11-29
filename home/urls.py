from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetCompleteView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register, name='register'),
    path('register_token/', views.register_with_token, name='register_token'),
    path('register_after_token/', views.register_after_token, name='register_after_token'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('change_user_details/', views.change_info, name='change_info'),
    path('reset_password/', PasswordResetView.as_view(), name='change_info'),
    path('reset_password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/complete/', PasswordResetCompleteView.as_view(extra_context={'login_url': '/login/'}), name='password_reset_complete'),
]