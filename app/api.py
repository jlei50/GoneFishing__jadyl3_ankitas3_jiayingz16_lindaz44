# GoneFishing: Jady Lei, Ankita Saha, Linda Zheng, Michelle Zhu
# P2: Open Waters
# SoftDev
# Jan 2025

import urllib.request
import json

from sitedb import *

# ======================================== #

# weather API documentation (no API keys required):
# https://open-meteo.com/en/docs

# example url:
# "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    
def getForecast(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&hourly=apparent_temperature&hourly=weather_code"
    data = urllib.request.urlopen(url)
    weather_dict = json.loads(data.read())
    temp = weather_dict["hourly"]["weather_code"]
    print(temp)

#getForecast(52.52,13.41)

# ======================================== #

def getWind():
    url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20210601&end_date=20210630&station=8724580&product=wind&time_zone=lst_ldt&interval=h&units=english&application=DataAPI_Sample&format=json"
    data = urllib.request.urlopen(url)
    response = json.loads(data.read())
    return response

# ======================================== #
def getRecipe():
    with open("keys/spoontacular.txt", "r") as file:
        api_key = file.read().strip()
    if not api_key:
        raise ValueError("API key file is empty. Please add a valid API key.")
    url = f'''https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query=fish'''
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(request)
    response = json.loads(data.read())
    return response
    

# ======================================== #

# ==============TESING========================== #
createUsers()
createGameSavesTable()
createLeaderboard()
addUser("ankita", "ankita")
p = returnEntireUsersTable()[0][0]
addGameStats(p, 9, "c", 4, 8, "c", 4)
updateDay(p, 4)
updateDay(p, 4)
updateDay(p, 4)
addVoyageLength(p, getVoyageLengthDays(p,4))

addUser("jady", "jady")
l = returnEntireUsersTable()[1][0]
addGameStats(l,89, "c", 4, 8, "c", 2)
updateDay(l, 2)
updateDay(l, 2)
updateDay(l, 2)
addVoyageLength(l, getVoyageLengthDays(l,2))

addUser("michelle","michelle")
v = returnEntireUsersTable()[2][0]
addGameStats(v,80, "c", 4, 8, "c", 3)
updateDay(v, 3)
updateDay(v, 3)
updateDay(v, 3)
addVoyageLength(v, getVoyageLengthDays(v,3))

addUser("linda","linda")
n = returnEntireUsersTable()[3][0]
addGameStats(n,59, "c", 4, 8, "c", 1)
updateDay(n, 1)
updateDay(n, 1)
updateDay(n, 1)
addVoyageLength(n, getVoyageLengthDays(n,1))



