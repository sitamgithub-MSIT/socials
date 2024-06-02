from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "", "id": "", "placeholder": "Full Name"}
        ),
        max_length=100,
        required=True,
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "", "id": "", "placeholder": "Username"}
        ),
        max_length=100,
        required=True,
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "", "id": "", "placeholder": "Mobile No."}
        ),
        max_length=100,
        required=True,
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"class": "", "id": "", "placeholder": "Email Address"}
        ),
        required=True,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "", "placeholder": "Password"}),
        required=True,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "", "placeholder": "Confirm Password"}),
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "full_name",
            "phone",
            "gender",
            "password1",
            "password2",
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "with-border"