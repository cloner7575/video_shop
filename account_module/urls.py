from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register_page'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('confirm/<phone_number>', views.ConfirmOtpView.as_view(), name='confirm_otp_page'),
    path('resend_otp', views.ResendOtpView.as_view(), name='resend_otp_page'),
    path('logout', views.LogoutView.as_view(), name='logout_page'),
    path('forget-pass', views.ForgetPasswordView.as_view(), name='forget_password_page'),
    path('reset-pass/<phone_number>', views.ResetPasswordView.as_view(), name='reset_password_page'),


]
