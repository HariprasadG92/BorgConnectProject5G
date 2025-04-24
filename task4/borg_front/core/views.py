from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('welcome'))
        else:
            return HttpResponse("Invalid login credentials")
    return render(request, "login.html")

def welcome_view(request):
    return render(request, "welcome.html")

def dashboard_view(request):
    return render(request, "dashboard.html")
