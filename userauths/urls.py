from django.urls import path, include
from userauths import views

app_name = "userauths"

urlpatterns = [
    path('user/sign-up/', views.register_view, name= "sign-up"),
    path('sign-up/', views.referral_signup, name='referral-signup'),
    path('user/sign-in/', views.login_view, name="sign-in"),
    path('user/forgot-password/', views.forgot_password, name="forgot-password"),
    path('get_user_data/', views.get_user_data, name='get_user_data'),
    path('trigger_daily_task/', views.trigger_daily_task, name='trigger_daily_task'),
    path('get_total_deposit/', views.get_total_deposit, name='get_total_deposit'),
    path('invalid-token/', views.email_invalid, name="invalid_token"),
    path('reset-password/<str:token>/', views.password_reset_form, name='password_reset_form'),
    path('process-password-reset/', views.process_password_reset, name='process_password_reset'),
    path('user/send-password-reset-email/', views.send_password_reset, name='send-password-reset-email'),
    path('password-reset-success/', views.password_reset_success, name="password-reset-success"),
    path('logout', views.logout_view, name="logout"),
    path('lockscreen', views.lock_screen_view, name='lockscreen'),
]

