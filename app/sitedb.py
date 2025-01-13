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
    command = "CREATE TABLE IF NOT EXISTS gameSaves (username TEXT, day INT, food INT, money INT, progress INT, crewMood TEXT)"
    c.execute(command)
    gameSaves.commit()

#use when first adding stas for user
def addGameStats(username, day, food, money, progress, crewMood):
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
        c.execute("INSERT INTO gameSaves (username, day, food, money, progress, crewMood) VALUES (?, ?, ?, ?, ?, ?)", (username, day, food, money, progress, crewMood))
        gameSaves.commit()
    return "game stats added"

#use once user stats in database
def saveGame(username, day, food, money, progress, crewMood):
    gameSaves = sqlite3.connect(USER_FILE)
    c = gameSaves.cursor()
    if (c.execute("SELECT 1 FROM userTable WHERE username=?", (username,))).fetchone():
        c.execute("UPDATE gameSaves set day=?, food=?, money=?, progress=?, crewMood=? WHERE username=?", (day, food, money, progress, crewMood, username))
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
# def addDay():

# def addMoney
<<<<<<< HEAD
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
=======

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
        c.execute("SELECT * FROM gameSaves WHERE username=?", (username))
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




>>>>>>> 6bea3dfd57e347b70e97c8ad811e45468058c2ff

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
