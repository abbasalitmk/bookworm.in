from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.signin, name='login'),
    path('verify-otp/', views.verify_otp, name='verify-otp'),
    path('logout', views.signout, name='logout'),
    path('resend-otp', views.resend_otp, name='resend-otp'),
    # path('forgot-password', views.forgot_password, name='forgot-password')
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify-email/', views.verify_email, name='verify-email'),
    path('reset_password', views.reset_password, name='reset_password')



]
