from django.urls import path, include
from . import views

urlpatterns = [
    path('weather/', views.WeatherView.as_view(), name='weather-info'),
]