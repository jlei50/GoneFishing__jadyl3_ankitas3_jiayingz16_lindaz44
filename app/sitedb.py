import sqlite3

USER_FILE="sea.db"

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

def deleteUsers():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("DROP table userTable")

def createGameSavesTable():
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    command = "CREATE TABLE IF NOT EXISTS gameSaves (username TEXT, day INT, food TEXT, money INT, progress INT, crewMood TEXT)"
    c.execute(command)
    gameSaves.commit()

def addGameStats(username, day, food, money, progress, crewMood):
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone() == None:
        c.execute("INSERT INTO gameSaves (username, day, food, money, progress, crewMood) VALUES (?, ?, ?, ?, ?, ? (username, day, food, money, progress, crewMood))")
        gameSaves.commit()
    return "game stats added"

def saveGame(username):
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone() == None:
        c.execute("UPDATE gameSaves set day=?, food=?, money=?, progress=?, crewMood=?, WHERE username=?", (day, food, money, progress, crewMood, username))
        gameSaves.commit()
    return "game stats added"

def getGameStats(username):
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone() == None:
        c.execute("SELECT * FROM gameSaves set day=?, food=?, money=?, progress=?, crewMood=?, WHERE username=?", (day, food, money, progress, crewMood, username))
        gameSaves.commit()
        return c.fetchone()
    
def getFinalVoyageLengthDays(username):
    days = sqlite3.connect(USER_FILE)
    c = days.cursor()
    #if progress from userTable == 100, return command, if not, return -1 --> in add voyagfe legnth, if voyage length -1, do not add
    command = "SELECT day FROM userTable"
    c.execute(command)
    return c.fetchall()

def createLeaderboard():
    leaderboardTable = sqlite3.connect(USER_FILE)
    c = leaderboardTable.cursor()
    command = "CREATE TABLE IF NOT EXISTS leaderboardTable (username TEXT, voyageLengthDays INTEGER)"
    c.execute(command)
    leaderboardTable.commit()
    
def addVoyageLength():
    leaderboardTable = sqlite3.connect(USER_FILE)
    c = leaderboardTable.cursor()
    command = "INSERT INTO leaderboardTable (username, voyageLengthDays) VALUES (?, ?)"
    c.execute(command)
    return

