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
#custom module
from sitedb import *
# from html_builder import *

# flask App
app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.secret_key = os.urandom(32)

@app.route("/")# checks for session and sends user to appropriate spot
def checkSession():
    # setup functions go here:
    createUsers()
    createGameSavesTable()

    return redirect("/home")
    # if 'username' in session:
    #     return redirect("/home")
    # return redirect("/login")

@app.route("/login", methods=["GET", "POST"])# will code registering and logging forms later
def login():
    if 'username' in session:
        return redirect("/home")

    print(returnEntireUsersTable())
    print("test")

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

    createGameSavesTable()

    stats = getGameStats(username)
    #print(stats)

    if not stats: # check if initial stats exist
        addGameStats(username, 2, 2, 1, 1, 'crewMood')

    saveGame(username, 2, 2, 1, 1, 'crewMood')

    #stop from randomizing wind and speed after each refresh
    if 'wind_speed' not in session or 'wind_dir' not in session:
        beegFile = api.getWind()
        data = (beegFile['data'])
        random_int = random.randint(1,700)
        day_data = (data[random_int])
        session['wind_speed'] = day_data['s']
        session['wind_dir'] = day_data['dr']
        print(session['wind_speed'])
        print(session['wind_dir'])
    else:
        print(session['wind_speed'])
        print(session['wind_dir'])

    day = getVoyageLengthDays(username);
    return render_template("game.html", speed=session['wind_speed'], direction=session['wind_dir'], day=day)

@app.route("/new_day")
def newDay():
    session.pop('wind_speed', None)
    session.pop('wind_dir', None)
    beegFile = api.getWind()
    data = (beegFile['data'])
    random_int = random.randint(1,700)
    day_data = (data[random_int])
    session['wind_speed'] = day_data['s']
    session['wind_dir'] = day_data['dr']
    return redirect("game")

@app.route("/logout")
def removeSession():
    session.pop('username', None)
    return redirect("/")

@app.route("/map")
def map():
    return render_template("map")

if __name__ == "__main__":
    app.debug = True
    app.run()
