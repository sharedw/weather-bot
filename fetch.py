import requests  # noqa
import yaml
import json


class DataFetcher():
    
    def __init__(self):
        self.DEVICE_URL = "https://api.ambientweather.net/v1/devices"
    
    def fetch_weather_data(self) -> dict:
        """Fetch weather data from Ambient Weather API."""
        url = "https://api.ambientweather.net/v1/devices"
        params = yaml.safe_load(open("secrets.yaml"))
        params = {k: params[k] for k in ("applicationKey", "apiKey")}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            curr_data = response.json()[0]["lastData"]
            print(curr_data)
        else:
            print("Error:", response.status_code, response.text)

        return curr_data
    
    def fetch_weatherapi_data(self):
        params = yaml.safe_load(open("secrets.yaml"))
        weatherapi_key = params['weatherapi']
        condition_url = f'http://api.weatherapi.com/v1/current.json?key={weatherapi_key}&q=31.1708409,-97.8459396&aqi=no'
        alert_url = f'http://api.weatherapi.com/v1/alerts.json?key={weatherapi_key}&q=31.1708409,-97.8459396'

        conditions = requests.get(condition_url)
        if conditions.status_code == 200:
            conditions = conditions.json()['current']['condition']
        
        alerts = requests.get(alert_url)
        if alerts.status_code == 200:
            alerts = alerts.json()['alerts']['alert']
            if len(alerts) > 0:
                conditions['alert'] = alerts[0]['headline']

        return conditions
    
    def fetch_all(self):
        curr_data = self.fetch_weather_data()
        curr_data.update(self.fetch_weatherapi_data())
        return curr_data
    
dfetcher = DataFetcher()
curr_data = dfetcher.fetch_all()

with open('sample_data.json', 'w') as f:
    json.dump(curr_data, f, indent=2)

