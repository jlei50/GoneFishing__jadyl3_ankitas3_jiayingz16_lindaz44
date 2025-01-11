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

# from sitedb import *
<<<<<<< HEAD
#from apis import *
=======
from api import *
>>>>>>> 6cc9195cc37373cba1cb2011dbb9953dfe22db7f
#custom module
from sitedb import *
# from apis import *
# from html_builder import *

# flask App
app = Flask(__name__, template_folder = "templates", static_folder = "../static")
app.secret_key = os.urandom(32)

@app.route("/")# checks for session and sends user to appropriate spot
def checkSession():
    # setup functions go here:
    createUsers()

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
    
def get_user_data(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    userData = c.fetchone()
    db.close()
    return userData

def test():
    createGameSavesTable()
    if 'username' in session:
        us = session['username']
        userData = get_user_data(us)
        if userData:
            print("User data:", userData)
            username = userData[0]
            addGameStats(username, 5, "corn", 5, 78, "sad")
            print(getGameStats(username))
        else:
            print("User not founddd")
        username = userData[0]
        addGameStats(username, 5, "corn", 5, 78, "sad")
        print(getGameStats(username))

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

@app.route("/game")
def game():
    return render_template("game")

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
