from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db.models.signals import post_save

from PIL import Image
from shortuuid.django_fields import ShortUUIDField
import shortuuid

# Create your models here.

GENDER = (("male", "Male"), ("female", "Female"))
RELATIONSHIP = (("single", "Single"), ("married", "Married"))


def user_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user.id, extension)
    return "user_{0}/{1}".format(instance.user.id, filename)


class User(AbstractUser):
    full_name = models.CharField(max_length=1000, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, choices=GENDER, blank=True, null=True)

    otp = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.username)


class UserProfile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvwxyz")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    cover_pic = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True, default="cover.jpg"
    )
    profile_pic = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True, default="default.jpg"
    )

    full_name = models.CharField(max_length=1000, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, choices=GENDER, blank=True, null=True)
    relationship = models.CharField(
        max_length=100, choices=RELATIONSHIP, blank=True, null=True, default="single"
    )
    bio = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(max_length=1000, blank=True, null=True)

    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)

    working_at = models.CharField(max_length=1000, blank=True, null=True)

    instagram = models.CharField(max_length=200, null=True, blank=True)
    whatsapp = models.CharField(max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False)

    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)
    blocked = models.ManyToManyField(User, related_name="blocked", blank=True)

    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        if self.full_name:
            return str(self.full_name)

        else:
            return str(self.user.username)

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            uuid = shortuuid.ShortUUID()
            unique_id = uuid.random(length=2)
            self.slug = slugify(self.full_name) + "-" + str(unique_id.lower())

        super(UserProfile, self).save(*args, **kwargs)


def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()


post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)
