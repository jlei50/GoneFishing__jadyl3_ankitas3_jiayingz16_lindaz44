# GoneFishing: Jady Lei, Ankita Saha, Linda Zheng, Michelle Zhu
# P2: Open Waters
# SoftDev
# Jan 2025

# imports
import os
import sqlite3
import json
import urllib.request
import datetime
import random

from flask import Flask, render_template, redirect, session, request, flash, jsonify

import api
import sitedb
#custom module
from sitedb import *
# from html_builder import *

# flask App
app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.secret_key = os.urandom(32)

@app.route("/")# checks for session and sends user to appropriate spot
def checkSession():
    # setup functions go here:
    runFunctions()

    return redirect("/home")
    # if 'username' in session:
    #     return redirect("/home")
    # return redirect("/login")

@app.route("/login", methods=["GET", "POST"])# will code registering and logging forms later
def login():
    if 'username' in session:
        return redirect("/home")

    if request.method =="POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:# checks if both form entries were filled out
            flash("Missing username/password", "error")
            return redirect("/login")

        if checkPass(username, password):# if password is correct, given user exists
            session["username"] = username# adds user to session
            return redirect("/game")

        else:# if password isnt correct
            flash("Invalid username/password", "error")
            return redirect("/login")

    return render_template("login.html")# if GET request, just renders login page


@app.route("/register", methods=["GET", "POST"])# will code registering and logging forms later
def register():
    if request.method =="POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:# checks if all 3 form entries were filled out
            return render_template("register.html", warning = "empty field(s)")

        #check if user has special chars
        #check for existing username
        message = addUser(username, password)
        if message:
            return render_template("register.html", warning = message)
        else:
            return redirect("/login")

    return render_template("register.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    return redirect("/home")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")

@app.route("/game")
def game():
    username = session.get('username')

    if not username:
        print("Error: Username not found in session.")
        return redirect('/login')

    stats = getGameStats(username)
    if not stats: # check if initial stats exist
        createGameSavesTable()
        day = 1
        food = 10
        crew = 20
        progress = 0
        crewMood = 'Calm'
        addGameStats(username, day, food, crew, progress, crewMood)
        saveGame(username, day, food, crew, progress, crewMood)  
    else: #references stats var otherwise
        saveGame(username, stats[1], stats[2], stats[3], stats[4], stats[5])
    
    #stop from randomizing wind and speed after each refresh
    if 'wind_speed' not in session or 'wind_dir' not in session:
        beegFile = api.getWind()
        data = (beegFile['data'])
        random_int = random.randint(1,700)
        day_data = (data[random_int])
        wind_speed = day_data['s']
        wind_dir = day_data['dr']
        if not wind_speed:
            wind_speed=2.2
        if not wind_dir:
            wind_dir="SE"
        session['wind_speed'] = wind_speed
        session['wind_dir'] = wind_dir
        print(session['wind_speed'])
        print(session['wind_dir'])
    else:
        print(session['wind_speed'])
        print(session['wind_dir'])
    
    courses = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW","SES", "SSE", "ESE", "ENE", "EEN"]
    session['course'] = courses[random.randint(0,20)]
    details = getGameStats(username)
    num_day = getVoyageLengthDays(username)
    return render_template("game.html", speed=session['wind_speed'], direction=session['wind_dir'], day=num_day, num_fish=details[2], crew=details[3], miles=round(details[4], 2), course=session['course'], progress=round((details[4]/30), 2))

@app.route("/sailChoice")
def sailChoice():
    print(session.get('wind_speed'))
    if session['wind_dir'] == session['course']:
        wind=1 #user heading in right direction, wind doesn't impact them
    if any(charA == charB for charA in session['wind_dir'] for charB in session['course']):
        wind=0.5 #wind slightly stopping user
    else:
        wind=-1 #user goes back bc of pushing winds

    progress = float(session.get('wind_speed'))*15*wind
    updateProgress(session.get('username'), progress)
    return redirect("/new_day")

@app.route("/new_day")
def newDay():
    session.pop('wind_speed', None)
    session.pop('wind_dir', None)
    if (random.randint(0,10)<5): #randomly depletes food
        updateFood(session['username'])
    if(getFood(session['username'])<=0):
        updateCrew(random.randint(0,3), session['username'])
    if(getCrew(session['username'])<=0):
        return render_template("end.html")
    if((getProgress(session['username'])/30)>=100):
        return render_template("win.html")
    beegFile = api.getWind()
    data = (beegFile['data'])
    random_int = random.randint(1,700)
    day_data = (data[random_int])
    wind_speed = day_data['s']
    wind_dir = day_data['dr']
    if not wind_speed:
        wind_speed=2.2
    if not wind_dir:
        wind_dir="SE"
    session['wind_speed'] = wind_speed
    session['wind_dir'] = wind_dir
    sitedb.updateDay(session['username'])
    return redirect("/game")

@app.route("/map")
def map():
    return render_template("map")

if __name__ == "__main__":
    app.debug = True
    app.run()