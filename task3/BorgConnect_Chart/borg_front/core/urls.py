from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('welcome/', views.welcome_view, name='welcome'),  # 👈 This renders dashboard.html
    path('api/chart-data/', views.get_chart_data, name='chart_data'),
]
