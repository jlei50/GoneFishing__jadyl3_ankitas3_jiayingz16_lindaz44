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
    print("hi")
    createUsers()
    createGameSavesTable()
    createLeaderboard()
    addUser("j", "j")
    p = returnEntireUsersTable()[0][0]
    print("username:" + p)
    addGameStats(p, 0, 3, 4, 8, "hf")
    saveGame(p, 9,3,0,0,"ftg")
    #updateVoyageLength(p, 4)
    #updateVoyageLength(p, 6)
    print("voyage days:" + str(getVoyageLengthDays(p)))
    print("updated voyage:" + str(getVoyageLengthDays(p)))
    print(getGameStats(p))
    print(returnSaveGamesTable())
    print(temp)

#getForecast(52.52,13.41)

# ======================================== #

def getWind():
    url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20210601&end_date=20210630&station=8724580&product=wind&time_zone=lst_ldt&interval=h&units=english&application=DataAPI_Sample&format=json"
    data = urllib.request.urlopen(url)
    response = json.loads(data.read())
    return response

# ======================================== #


# ======================================== #
