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
    return "Username added"

def checkPass(username, password):
    userTable = sqlite3.connect(USER_FILE)
    c = userTable.cursor()
    c.execute("SELECT password FROM userTable WHERE username=?", (username,))
    f = c.fetchone()
    if (password == f[0]):
        return True
    return "Invalid login"

def checkUser(username, password):
    userTable = sqlite3.connect(USER_FILE)
    c = userTable.cursor()
    c.execute("SELECT username FROM userTable WHERE password=?", (password,))
    f = c.fetchone()
    if (username == f[0]):
        return True
    return "Invalid login"

def deleteUsers():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("DROP table userTable")