# GoneFishing: Jady Lei, Ankita Saha, Linda Zheng, Michelle Zhu
# P2: Open Waters
# SoftDev
# Jan 2025

import urllib.request
import json

# ======================================== #

# weather API documentation (no API keys required):
# https://open-meteo.com/en/docs

# example url:
# "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

forecast = f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41"

data = urllib.request.urlopen(forecast)
print(json.loads(data.read()))

def getForecast(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&hourly=apparent_temperature&hourly=weather_code"
    data = urllib.request.urlopen(url)
    weather_dict = json.loads(data.read())
    temp = weather_dict["hourly"]["weather_code"]
    print(temp)

getForecast(52.52,13.41);

# ======================================== #
"""
template for later

def fetch_openweather(lat, lon):
    with open("keys/key_OpenWeatherMap.txt", "r") as file:
        api_key = file.read().strip()
    if not api_key:
        raise ValueError("API key file is empty. Please add a valid API key.")
    response = requests.get(f'''http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt=40&units=imperial&appid={api_key}''')
    if response.status_code == 200:
        return response.json()
"""


# ======================================== #


# ======================================== #