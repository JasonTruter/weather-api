from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
import requests
import copy

class WeatherView(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        city = self.request.query_params.get('city')
        period = self.request.query_params.get('period')
        if not city or not period:
            return Response({"error": "missing querystring params 'city' and/or 'period'"}, status.HTTP_400_BAD_REQUEST)
        
        resp = self.get_weather_from_public_api(city, period)
        error = resp.get('error')
        if error:
            errorcode = error['code']
            if errorcode:
                if errorcode == 1007:
                    return Response({"error": "period should be in 'yyyy-MM-dd' format and on or after 1st Jan, 2015"}, status.HTTP_400_BAD_REQUEST)
                elif errorcode == 1008:
                    return Response({"error": "api is limited to 30 days history"}, status.HTTP_400_BAD_REQUEST)
                    
        return Response(self.process_resp(resp), status.HTTP_200_OK)

    def get_weather_from_public_api(self, city, period):
        url = "http://api.weatherapi.com/v1/history.json"
        querystring = {"key":"8e4ba672f5844bebaa5144433202408","q": city,"dt":period}
        response = requests.request("GET", url, params=querystring)
        return response.json()

    def process_resp(self, resp):
        processed = {}

        resp_copy = copy.deepcopy(resp)
        hours_arr = resp['forecast']['forecastday'][0]['hour']
        temps = self.get_temps(hours_arr)
        humidity = self.get_humidity(hours_arr)
        
        processed['avg_temp'] = self.calc_average(temps)
        processed['median_temp'] = self.calc_median(temps)
        processed['min_temp'] = min(temps)
        processed['max_temp'] = max(temps)

        processed['avg_humidity'] = self.calc_average(humidity)
        processed['median_humidity'] = self.calc_median(humidity)
        processed['min_humidity'] = min(humidity)
        processed['max_humidity'] = max(humidity)

        return processed

    def get_temps(self, hours):
        temps = []
        for hour in hours:
            temps.append(hour['temp_c'])
        return temps

    def get_humidity(self, hours):
        humidity = []
        for hour in hours:
            humidity.append(hour['humidity'])
        return humidity

    def calc_average(self, n_num):
        print('Average:'+str(n_num))
        average = sum(n_num) / len(n_num)
        return average

    def calc_median(self, n_num):
        print('Median:'+str(n_num))
        n = len(n_num) 
        n_num.sort() 
        
        if n % 2 == 0: 
            median1 = n_num[n//2] 
            median2 = n_num[n//2 - 1] 
            median = (median1 + median2)/2
        else: 
            median = n_num[n//2] 
        return median