from django.urls import path, include
from userauths import views

app_name = "userauths"

urlpatterns = [
    path('user/sign-up/', views.register_view, name= "sign-up"),
    path('user/sign-in/', views.login_view, name="sign-in"),
    path('logout', views.logout_view, name="logout"),
    path('lockscreen', views.lock_screen_view, name='lockscreen'),
]

