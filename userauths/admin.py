from django.contrib import admin
from userauths.models import User, UserProfile


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "full_name", "email", "gender"]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "full_name", "verified"]
    list_editable = ["verified"]


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
