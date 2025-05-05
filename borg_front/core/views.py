from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import redis
import json
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

@login_required
def dashboard_view(request):
    # Get current settings from Redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    settings = redis_client.get('dashboard_settings')
    
    context = {
        'current_settings': json.loads(settings) if settings else {
            'sampling_type': 'avg',
            'sampling_freq': 5,
            'status': 'stopped'
        }
    }
    return render(request, "dashboard.html", context)

@csrf_exempt
def update_settings(request):
    if request.method == 'POST':
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
        # Get current settings or create default
        current_settings = redis_client.get('dashboard_settings')
        if current_settings:
            current_settings = json.loads(current_settings)
        else:
            current_settings = {
                'sampling_type': 'avg',
                'sampling_freq': 5,
                'status': 'stopped'
            }
        
        # Update with new values
        data = json.loads(request.body)
        for key in data:
            current_settings[key] = data[key]
        
        # Save to Redis
        redis_client.set('dashboard_settings', json.dumps(current_settings))
        
        return JsonResponse(current_settings)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def get_settings(request):
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    settings = redis_client.get('dashboard_settings')
    if settings:
        return JsonResponse(json.loads(settings))
    return JsonResponse({
        'sampling_type': 'avg',
        'sampling_freq': 5,
        'status': 'stopped'
    })