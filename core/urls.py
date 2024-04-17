from django.urls import path
from core import views

urlpatterns = [
    path("", views.homepageview, name="homepageview"),
]