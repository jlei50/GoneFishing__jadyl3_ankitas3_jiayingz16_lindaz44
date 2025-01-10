# GoneFishing: Jady Lei, Ankita Saha, Linda Zheng, Michelle Zhu
# P2: Open Waters
# SoftDev
# Jan 2025

import urllib.request
import json

# ======================================== #

# weather API documentation:
# https://open-meteo.com/en/docs

# example url:
# "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

forecast = f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41"

data = urllib.request.urlopen(forecast)
print(json.loads(data.read()))

# ======================================== #
