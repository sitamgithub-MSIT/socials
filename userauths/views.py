from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


from userauths.forms import UserRegistrationForm
from userauths.models import UserProfile, User

# Create your views here.


def registerpageview(request):

    if request.user.is_authenticated:
        messages.warning(request, f"Hi {request.user.full_name}, You are already logged in!")
        return redirect("core:homepageview")

    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get("full_name")
        phone = form.cleaned_data.get("phone")
        email = form.cleaned_data.get("email")
        gender = form.cleaned_data.get("gender")
        password = form.cleaned_data.get("password1")


        user = authenticate(username=email, password=password)
        login(request, user)

        messages.success(
            request, f"Welcome {full_name}, Your account has been created successfully!"
        )

        profile = UserProfile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.gender = gender

        profile.save()
        return redirect("core:homepageview")

    context = {"form": form}
    return render(request, "userauths/register.html", context)


def loginpageview(request):

    if request.user.is_authenticated:
        messages.warning(request, f"Hi {request.user.full_name}, You are already logged in!")
        return redirect("core:homepageview")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in successfully!")
                return redirect("core:homepageview")
            else:
                messages.error(request, "Username OR Password is incorrect!")
                return redirect("userauths:registerpageview")

        except:
            messages.error(request, "User does not exist!")
            return redirect("userauths:registerpageview")

    return HttpResponseRedirect("/")


def logoutpageview(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect("userauths:registerpageview")