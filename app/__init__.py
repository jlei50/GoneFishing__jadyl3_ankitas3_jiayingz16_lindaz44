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
            return redirect("/home")

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
    username = session.get('username')
    saveHtml = "No account detected."
    path = request.path
    if path == "/home":
        if not username:
            print("Error: Username not found in session.")
            return redirect('/login')
        ukey = getNumGamesPlayed(username)
        ukey+=1
        addGameStats(username, 1, 20,2, 0, 'Calm', ukey)
        stats = getGameStats(username, ukey)
    if username:
        saves = getAllGameStats(username)
        saveHtml = returnSavesHtml(saves)
    savenum = "/" + str(getKey(username) + 1)
    return render_template("home.html", saves = saveHtml, linknum = savenum)

@app.route("/leaderboard")
def leaderboard():
    username = session.get('username')
    if voyageFinished(username):
        addVoyageLength(username)
    num = []
    for i in range(len(top10())):
            num.append(i)
    return render_template('leaderboard.html', arr=top10(), num=num)

@app.route("/game")
def game():
    username = session.get('username')
    ukey = session.get('ukey')
    session['died'] = False
    ukey = getNumGamesPlayed(username)
    path = request.path
    if path == "/game":
        if not username:
            print("Error: Username not found in session.")
            return redirect('/login')

    stats = getGameStats(username)
    print(stats)
    if not stats or session['died'] == True or len(stats) < 7: # check if initial stats exist
        createGameSavesTable()
        day = 1
        food = 10
        crew = 20
        progress = 0
        crewMood = 'Calm'
        ukey = 0
        addGameStats(username, day, food, crew, progress, crewMood, ukey)
        saveGame(username, day, food, crew, progress, crewMood, ukey)  
    else: #references stats var otherwise
        saveGame(username, stats[1], stats[2], stats[3], stats[4], stats[5], stats[6])
    
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
    
    return render_template("game.html", speed=session['wind_speed'], direction=session['wind_dir'], day=num_day, num_fish=details[2], crew=details[3], miles=round(details[4], 2), course=session['course'], progress=round((details[4]/30), 2), crewMood=details[5])

@app.route("/sailChoice")
def sailChoice():
    username = session.get('username')
    print(session.get('wind_speed'))
    ukey = session.get('ukey')
    if session['wind_dir'] == session['course']:
        wind=1 #user heading in right direction, wind doesn't impact them
    if any(charA == charB for charA in session['wind_dir'] for charB in session['course']):
        wind=0.5 #wind slightly stopping user
    else:
        wind=0.1 #user doesn't move much

    progress = float(session.get('wind_speed'))*15*wind
    updateProgress(session.get('username'), progress)
    return redirect("/new_day")

@app.route("/fishChoice")
def fishChoice():
    username = session.get('username')
    stats = getGameStats(username)
    wind = session.get('wind_speed')
    fish = stats[2]
    crew = stats[3]
    
    if(crew >= 10 and wind==1):
        fish += 5
    if(crew >=10 and wind==0.5):
        fish += 2
    else:
        fish += 1
        
    progress = float(fish)
    saveGame(username, stats[1], fish, stats[3], stats[4], stats[5], stats[6])
    updateProgress(username, progress)
    return redirect("/new_day")

@app.route("/new_day")
def newDay():
    session.pop('wind_speed', None)
    session.pop('wind_dir', None)
    if (random.randint(0,10)<7): #randomly depletes food
        updateFood(session['username'])
    if(getFood(session['username'])<=0):
        updateCrew(random.randint(0,3), session['username'])
    if(getCrew(session['username'])<=0):
        session['died'] = True
        newGame(session['username'], getKey(session['username']) +1)
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

@app.route("/saveExitGame")
def saveExitGame():
    username = session.get('username')
    stats = getGameStats(username)
    saveGame(username, stats[1], stats[2], stats[3], stats[4], stats[5], stats[6])
    return render_template("home.html", day = stats[1], food = stats[2], crew = stats[3], progress = stats[4], crewMood = stats[5], numPlayed = stats[6]+1)

# @app.route("/newGame")
# def resetGame():
#     username = session.get('username')
#     ukey = session.get('ukey')
#     stats = getGameStats(username, ukey)
#     saveGame(username, stats[1], stats[2], stats[3], stats[4], stats[5], stats[6])
#     return render_template("home.html", day = stats[1], food = stats[2], crew = stats[3], progress = stats[4], crewMood = stats[5], numPlayed = stats[6]+1)

@app.route("/0")
def one():
    session["ukey"] = 0
    return redirect("/game")

@app.route("/1")
def two():
    session["ukey"] = 1
    return redirect("/game")

@app.route("/2")
def three():
    session["ukey"] = 2
    return redirect("/game")

@app.route("/3")
def four():
    session["ukey"] = 3
    return redirect("/game")

@app.route("/4")
def five():
    session["ukey"] = 4
    return redirect("/game")

@app.route("/5")
def six():
    session["ukey"] = 5
    return redirect("/game")

# html builders
def returnSavesHtml(saves):
    '''
    <div class="card">
      <div class="card-header">
        Game Save [TODO num]
      </div>
      <div class="card-body row">
        <div class="col-10">
            <h6 class="card-text fs-6">Day: []</h6>
            <h6 class="card-text fs-6">Progress: []</h6>
        </div>
        <div class="col d-flex flex-row-reverse">
            <a href="#" class="btn btn-primary d-flex align-items-center">Load</a>
        </div>
      </div>
    </div>
    '''
    output = ""
    if saves:
        for save in saves:
            output += f'''
                <div class="card">
                <div class="card-header">
                    Game Save {save[6]}
                </div>
                <div class="card-body row">
                    <div class="col-8">
                        <h6 class="card-text fs-6">Day: {save[1]}</h6>
                        <h6 class="card-text fs-6">Progress:{int(save[4]/30)}</h6>
                    </div>
                    <div class="col d-flex flex-row-reverse">
                        <a href="/{save[6]}" class="btn btn-primary d-flex align-items-center">Load</a>
                    </div>
                </div>
                </div>
            '''
        return output
    else:
        return "No Saves Created"

if __name__ == "__main__":
    app.debug = True
    app.run()