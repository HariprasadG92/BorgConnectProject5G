from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('update_settings/', views.update_settings, name='update_settings'),
    path('get_settings/', views.get_settings, name='get_settings'),
]