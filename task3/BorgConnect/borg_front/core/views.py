from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import redis
from django.conf import settings

# Initialize Redis client
def get_redis_client():
    return redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )

# Store Redis client for reuse
redis_client = get_redis_client()

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Decode the JSON payload
            username = data.get("username")
            password = data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("success")
            else:
                return HttpResponse("Invalid login credentials", status=401)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)  # In case of bad JSON
    return render(request, "login.html")

def welcome_view(request):
    # Hardcoded instance_id used in the pipeline
    instance_id = "123456"

    try:
        # Try fetching data from Redis
        data = redis_client.get(instance_id)
        if data:
            data = json.loads(data)
            content = f"""
            <h2>Welcome to Borg Connect</h2>
            <p><strong>Instance ID:</strong> {instance_id}</p>
            <p><strong>Sampling Type:</strong> {data.get('sampling_type')}</p>
            <p><strong>Sampling Frequency:</strong> {data.get('sampling_frequency')}</p>
            <p><strong>Sampled Value:</strong> {data.get('value')}</p>
            """
        else:
            content = "<h2>Welcome to Borg Connect</h2><p>No data available in Redis.</p>"

        return HttpResponse(content)
    
    except redis.ConnectionError:
        return HttpResponse("Error connecting to Redis", status=500)
