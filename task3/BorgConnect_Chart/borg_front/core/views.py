from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .redis_client import get_sampled_data

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "dashboard.html")  # ⬅️ render dashboard instead of HttpResponse
        else:
            return HttpResponse("Invalid login credentials", status=401)
    return render(request, "login.html")

def welcome_view(request):
    return render(request, "dashboard.html")

@csrf_exempt
def get_chart_data(request):
    data = get_sampled_data()
    return JsonResponse(data)
