from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.registerpageview, name="registerpageview"),
    path("sign-in/", views.loginpageview, name="loginpageview"),
    path("sign-out/", views.logoutpageview, name="logoutpageview"),
]