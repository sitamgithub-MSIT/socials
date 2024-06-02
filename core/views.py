from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

#@login_required
def homepageview(request):
    return render(request, "core/home.html")