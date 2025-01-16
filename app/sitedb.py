import sqlite3
import random

USER_FILE="sea.db"

def runFunctions():
    createUsers()
    createGameSavesTable()
    createLeaderboard()

def createUsers():
    userTable = sqlite3.connect(USER_FILE)
    c = userTable.cursor()
    command = "CREATE TABLE IF NOT EXISTS userTable (username TEXT, password TEXT)"
    c.execute(command)
    userTable.commit()

def addUser(username, password):
    userTable = sqlite3.connect(USER_FILE)
    c = userTable.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone() == None:
        c.execute("INSERT INTO userTable (username, password) VALUES (?, ?)", (username, password))
        userTable.commit()
        return
    # return "Username added"

def checkPass(username, password):
    userTable = sqlite3.connect(USER_FILE)
    c = userTable.cursor()
    c.execute("SELECT password FROM userTable WHERE username=?", (username,))
    f = c.fetchone()
    print(f)
    if (f == None):
        return False
    if ( password != f[0]):
        return False
    return True

def checkUser(username, password):
    userTable = sqlite3.connect(USER_FILE)
    c = userTable.cursor()
    c.execute("SELECT username FROM userTable WHERE password=?", (password,))
    f = c.fetchone()
    if (username == f[0]):
        return True
    return "Invalid login"

# dev stuff
def returnEntireUsersTable():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM userTable")
    return c.fetchall()

def getUserInfo(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    userData = c.fetchone()
    db.close()
    return userData

def deleteUsers():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("DROP table userTable")

def createGameSavesTable():
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    command = "CREATE TABLE IF NOT EXISTS gameSaves (username TEXT, day INT, food INT, crew INT, progress REAL, crewMood TEXT, ukey INT)"
    c.execute(command)
    gameSaves.commit()

#use when first adding stas for user
def addGameStats(username, day, food, crew, progress, crewMood, ukey):
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
        c.execute("INSERT INTO gameSaves (username, day, food, crew, progress, crewMood, ukey) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, day, food, crew, progress, crewMood, ukey))
        gameSaves.commit()
    return "game stats added"

#use once user stats in database
def saveGame(username, day, food, crew, progress, crewMood, ukey):
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
        c.execute("UPDATE gameSaves set day=?, food=?, crew=?, progress=?, crewMood=?, ukey=? WHERE username=?", (day, food, crew, progress, crewMood, ukey, username))
        gameSaves.commit()
    return "game stats added"

def returnSaveGamesTable():
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    c.execute("SELECT * FROM gameSaves")
    return c.fetchall()

def getGameStats(username, ukey):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    # check if username exists in gameSaves
    c.execute("SELECT * FROM gameSaves WHERE username=?AND ukey=?", (username, ukey))
    userGameData = c.fetchone()
    return list(userGameData) if userGameData else None

def getAllGameStats(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    # check if username exists in gameSaves
    c.execute("SELECT * FROM gameSaves WHERE username=?", (username,))
    userGameData = c.fetchall()
    return list(userGameData) if userGameData else None

def updateDay(username, ukey):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT day FROM gameSaves WHERE username = ? AND ukey=?", (username, ukey))
    data = c.fetchone()
    day = data[0]+1
    c.execute("UPDATE gameSaves SET day = ? WHERE username = ? AND ukey=?", (day, username, ukey))
    db.commit()

def updateProgress(username, miles, ukey):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT progress FROM gameSaves WHERE username = ? AND ukey=?", (username, ukey))
    data = c.fetchone()
    totalMiles = data[0]+miles
    c.execute("UPDATE gameSaves SET progress = ? WHERE username = ? AND ukey=?", (totalMiles, username, ukey))
    db.commit()

def updateFood(username, food, ukey):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("UPDATE gameSaves SET food = ? WHERE username = ? AND ukey=?", (food, username, ukey))
    db.commit()

def getFood(username, ukey):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT food FROM gameSaves WHERE username = ? AND ukey=?", (username, ukey))
    data = c.fetchone()
    food = data[0]
    return food

def updateCrew(deaths, username, ukey):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT crew FROM gameSaves WHERE username = ? AND ukey=?", (username, ukey))
    data = c.fetchone()
    crew = data[0]
    if not(data[0]==0):
        crew = data[0]-deaths
    c.execute("UPDATE gameSaves SET crew = ? WHERE username = ? AND ukey=?", (crew, username, ukey))
    db.commit()

def getCrew(username, ukey):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT crew FROM gameSaves WHERE username=?  AND ukey=?", (username, ukey))
    data = c.fetchone()
    crew = data[0]
    return crew

def getKey(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT ukey FROM gameSaves WHERE username = ? ORDER BY ukey DESC", (username,))
    data = c.fetchone()
    if data:
        key = data[0]
    else:
        key = 0
    return key


def createLeaderboard():
    leaderboardTable = sqlite3.connect(USER_FILE)
    c = leaderboardTable.cursor()
    command = "CREATE TABLE IF NOT EXISTS leaderboardTable (username TEXT, voyageLengthDays INTEGER)"
    c.execute(command)
    leaderboardTable.commit()
    
def getVoyageLengthDays(username, ukey):
    days = sqlite3.connect(USER_FILE)
    c = days.cursor()
    c.execute("SELECT day FROM gameSaves WHERE username=? AND ukey=?", (username, ukey))
    day = c.fetchone()
    return day[0]

def getProgress(username, ukey):
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
        c.execute("SELECT * FROM gameSaves WHERE username=? AND ukey=?", (username, ukey))
        userProgress = c.fetchone()[3]
        return userProgress

def addVoyageLength(username, voyageLengthDays, ukey):
    leaderboardTable = sqlite3.connect(USER_FILE)
    c = leaderboardTable.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
        c.execute("INSERT INTO leaderboardTable (username, voyageLengthDays) VALUES (?, ?)", (username,getVoyageLengthDays(username, ukey)))
        leaderboardTable.commit()
    return "game stats added"



def voyageFinished(username, ukey):
    return (getProgress(username, ukey) == 100)

def finalVoyageLength(username, ukey):
    return getVoyageLengthDays(username, ukey)
    
def returnLeaderboardStats(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    # check if username exists in gameSaves
    c.execute("SELECT * FROM leaderboardTable WHERE username=?", (username,))
    leaderboardT = c.fetchone()
    return list(leaderboardT) if leaderboardT else None

def top10():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    # check if username exists in gameSaves
    c.execute("SELECT * FROM leaderboardTable")
    leaderboardT = sorted(c.fetchall()[:10], reverse=True)
    return leaderboardT

def newGame(username, key):
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
        c.execute("INSERT INTO gameSaves (username, day, food, crew, progress, crewMood, ukey) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, 0, 10, 20, 0, "calm", getKey(username)+1))
        gameSaves.commit()
    return "new game"
        



#     TESTING
#     print("hi")
#     createUsers()
#     createGameSavesTable()
#     addUser("j", "j")
#     p = returnEntireUsersTable()[2][0]
#     print("username:" + p)
#     addGameStats(p, 0, "fg", 4, 8, "hf")
#     saveGame(p, 9,"lllllllllllll",0,0,"ftg")
#     print(getGameStats(p))
#     print(returnSaveGamesTable())

