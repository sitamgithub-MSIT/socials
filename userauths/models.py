from django.db import models
from django.contrib.auth.models import AbstractUser

from PIL import Image
from shortuuid.django_fields import ShortUUIDField

# Create your models here.

GENDER = (("male", "Male"), ("female", "Female"))
RELATIONSHIP = (("single", "Single"), ("married", "Married"))


def user_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user.id, extension)
    return f"user_{instance.user.id}/{filename}"


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


class UserProfile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvwxyz")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    cover_pic = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True, default="cover.jpg"
    )
    profile_pic = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True, default="default.jpg"
    )

    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, default="male")
    relationship = models.CharField(
        max_length=100, choices=RELATIONSHIP, default="single"
    )
    bio = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    country = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    working_at = models.CharField(max_length=200, null=True, blank=True)

    instagram = models.CharField(max_length=200, null=True, blank=True)
    whatsapp = models.CharField(max_length=200, null=True, blank=True)
    verified = models.BooleanField(default=False)

    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)
    blocked = models.ManyToManyField(User, related_name="blocked", blank=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
