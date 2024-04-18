from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

GENDER = (("male", "Male"), ("female", "Female"))


class User(AbstractUser):
    full_name = models.CharField(max_length=200)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200)
    gender = models.CharField(max_length=100, choices=GENDER)

    otp = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
