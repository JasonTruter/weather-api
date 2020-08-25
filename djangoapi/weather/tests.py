from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

# User story:
# As an API user I want to get min, max, average and median temperature 
# and humidity for given city and period of time

class WeatherViewTestCase(APITestCase):

    weather_url = reverse('weather-info')

    def test_should_error_when_no_city_and_period(self):
        response = self.client.get(self.weather_url)        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "missing querystring params 'city' and/or 'period'")
    
    def test_should_error_when_period_is_less_than_2015(self):
        response = self.client.get(self.weather_url, {'city': 'Durban', 'period': '2014-02-02'})        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "period should be in 'yyyy-MM-dd' format and on or after 1st Jan, 2015")
    