import sqlite3

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
    command = "CREATE TABLE IF NOT EXISTS gameSaves (username TEXT, day INT, food INT, crew INT, progress REAL, crewMood TEXT)"
    c.execute(command)
    gameSaves.commit()

#use when first adding stas for user
def addGameStats(username, day, food, crew, progress, crewMood):
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
        c.execute("INSERT INTO gameSaves (username, day, food, crew, progress, crewMood) VALUES (?, ?, ?, ?, ?, ?)", (username, day, food, crew, progress, crewMood))
        gameSaves.commit()
    return "game stats added"

#use once user stats in database
def saveGame(username, day, food, crew, progress, crewMood):
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
        c.execute("UPDATE gameSaves set day=?, food=?, crew=?, progress=?, crewMood=? WHERE username=?", (day, food, crew, progress, crewMood, username))
        gameSaves.commit()
    return "game stats added"

def returnSaveGamesTable():
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    c.execute("SELECT * FROM gameSaves")
    return c.fetchall()

def getGameStats(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    # check if username exists in gameSaves
    c.execute("SELECT * FROM gameSaves WHERE username=?", (username,))
    userGameData = c.fetchone()
    return list(userGameData) if userGameData else None

def updateDay(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT day FROM gameSaves WHERE username = ?", (username,))
    data = c.fetchone()
    day = data[0]+1
    c.execute("UPDATE gameSaves SET day = ? WHERE username = ?", (day, username))
    db.commit()

def updateProgress(username, miles):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT progress FROM gameSaves WHERE username = ?", (username,))
    data = c.fetchone()
    totalMiles = data[0]+miles
    c.execute("UPDATE gameSaves SET progress = ? WHERE username = ?", (totalMiles, username))
    db.commit()

def updateFood(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT food FROM gameSaves WHERE username = ?", (username,))
    data = c.fetchone()
    food = data[0]
    if not(data[0]==0):
        food = data[0]-1
    c.execute("UPDATE gameSaves SET food = ? WHERE username = ?", (food, username))
    db.commit()

def getFood(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT food FROM gameSaves WHERE username = ?", (username,))
    data = c.fetchone()
    food = data[0]
    return food

def updateCrew(deaths, username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT crew FROM gameSaves WHERE username = ?", (username,))
    data = c.fetchone()
    crew = data[0]
    if not(data[0]==0):
        crew = data[0]-deaths
    c.execute("UPDATE gameSaves SET crew = ? WHERE username = ?", (crew, username))
    db.commit()

def getCrew(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT crew FROM gameSaves WHERE username = ?", (username,))
    data = c.fetchone()
    crew = data[0]
    return crew

# def addCrew
# 
# def createLeaderboard():
#     leaderboardTable = sqlite3.connect(USER_FILE)
#     c = leaderboardTable.cursor()
#     command = "CREATE TABLE IF NOT EXISTS leaderboardTable (username TEXT, voyageLengthDays INTEGER)"
#     c.execute(command)
#     leaderboardTable.commit()
#     
# def getVoyageLengthDays(username):
#     days = sqlite3.connect(USER_FILE)
#     c = days.cursor()
#     c.execute("SELECT day FROM gameSaves WHERE username=?", (username,))
#     day = c.fetchone()
#     return day[0]
# 
# def getProgress(username):
#     gameSaves = sqlite3.connect(USER_FILE)
#     c = gameSaves.cursor()
#     if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
#         c.execute("SELECT * FROM gameSaves WHERE username=?", (username))
#         userProgress = c.fetchone()[3]
#         return userProgress
# 
# def addVoyageLength(username, voyageLengthDays):
#     leaderboardTable = sqlite3.connect(USER_FILE)
#     c = leaderboardTable.cursor()
#     if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
#         c.execute("INSERT INTO leaderboardTable (username, voyageLengthDays) VALUES (?, ?)", (username, voyageLengthDays))
#         leaderboardTable.commit()
#     return 
# 
# def updateVoyageLength(username, day):
#     leaderboardTable = sqlite3.connect(USER_FILE)
#     c = leaderboardTable.cursor()
#     if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
#         c.execute("UPDATE leaderboardTable set voyageLengthDays=?, WHERE username=?", (day+getVoyageLengthDays(username), username))
#         leaderboardTable.commit()
#     
# def voyageFinished(username):
#     return (getProgress(username) == 100)
# 
# def finalVoyageLength(usrename):
#     if voyageFinished():
#         return getVoyageLengthDays(username)
# 
# 
# 
# 


def createLeaderboard():
    leaderboardTable = sqlite3.connect(USER_FILE)
    c = leaderboardTable.cursor()
    command = "CREATE TABLE IF NOT EXISTS leaderboardTable (username TEXT, voyageLengthDays INTEGER)"
    c.execute(command)
    leaderboardTable.commit()
    
def getVoyageLengthDays(username):
    days = sqlite3.connect(USER_FILE)
    c = days.cursor()
    c.execute("SELECT day FROM gameSaves WHERE username=?", (username,))
    day = c.fetchone()
    return day[0]

def getProgress(username):
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
        c.execute("SELECT * FROM gameSaves WHERE username=?", (username,))
        userProgress = c.fetchone()[3]
        return userProgress

def addVoyageLength(username, voyageLengthDays):
    leaderboardTable = sqlite3.connect(USER_FILE)
    c = leaderboardTable.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
        command = "INSERT INTO leaderboardTable (username, voyageLengthDays) VALUES (?, ?)"
        c.execute(command)
        leaderboardTable.commit()
    return "game stats added"

def voyageFinished(username):
    return (getProgress(username) == 100)

def finalVoyageLength(usrename):
    if voyageFinished():
        return getVoyageLengthDays(username)




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