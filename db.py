from flask import Flask, render_template, request,  session, redirect, url_for, flash
import sqlite3 # enable control of an sqlite database

userID = -1

def addUser(): #adds user to database
    if request.form['password'] != request.form['password2']:
        flash("Error! Passwords do not match")
        return False
    else:
        dbfile = "data.db"
        db = sqlite3.connect(dbfile)
        c = db.cursor() #standard connection
        command = "SELECT COUNT(*) FROM users WHERE username = \"{}\";"
        newUser = c.execute(command.format(request.form['username'])) #execution of sqlite command with the given username instead of the brackets
        for bar in newUser:
            if bar[0] > 0: #if username exists
                flash("Username is already taken. Please choose another one.")
                return False
            else:
                id = getTableLen("users") #gives the user the next availabe id
                c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?);", (id, request.form['username'], request.form['password'], request.form['firstName'], request.form['lastName'], "", "")) #different version of format
                db.commit()
                c.execute("INSERT INTO apiKeys VALUES(?, ?, ?, ?);", (id, "", "", ""))
                db.commit()
                db.close()
                flash("Register Success!")
                flash("index")
                return True

def login(): #login function
    global userID
    dbfile = "data.db"
    db = sqlite3.connect(dbfile)
    c = db.cursor()
    command = "SELECT * FROM users WHERE username = \"{}\";"
    listUsers = c.execute(command.format(request.form['username'])) #fills in brackets with the given username and executes it in sqlite
    bar = list(enumerate(listUsers))
    if len(bar) > 0: #checks whether there exists a user with the given username
        getPass = "SELECT password FROM users WHERE username = \"{}\";"
        listPass = c.execute(getPass.format(bar[0][1][1]))
        for p in listPass:
            if request.form['password'] == p[0]: #compare passwords
                userID = bar[0][1][0]
                return True
            else:
                flash("Error! Incorrect password")
                return False
    else:
        flash("Error! Username does not exist")
        return False

def update(): #updates a user's info based on the info provided
    dbfile = "data.db"
    db = sqlite3.connect(dbfile)
    c = db.cursor()
    blank = True
    arr = ['firstName','lastName','username','password','location', 'address']
    idx = 0
    while idx < len(arr):
        if request.form[arr[idx]] != "":
            command = "UPDATE users SET {} = \"{}\" WHERE id = {};"
            c.execute(command.format(arr[idx],request.form[arr[idx]],userID))
            blank = False
            db.commit()
        idx += 1
    if not blank:
        flash("Update Success!")
    else:
        flash("Nothing has been updated.")
    db.commit()
    db.close()

def getTableLen(tbl): #returns the length of a table
    dbfile = "data.db"
    db = sqlite3.connect(dbfile)
    c = db.cursor()
    command = "SELECT COUNT(*) FROM {};"
    q = c.execute(command.format(tbl))
    for line in q:
        return line[0]

def fillUserInfo(arr): #@param arr is an array and fills this array with info on the current user
    dbfile = "data.db"
    db = sqlite3.connect(dbfile)
    c = db.cursor()
    q = c.execute("SELECT * FROM users WHERE id = {};".format(userID))
    for bar in q:
        arr['username'] = bar[1]
        arr['firstName'] = bar[3]
        arr['lastName'] = bar[4]
        arr['location'] = bar[5]
        arr['address'] = bar[6]

def updateAPIKey(button): #@param button determines which API to get updated
    dbfile = "data.db"
    db = sqlite3.connect(dbfile)
    c = db.cursor()
    arr = ['openWeather', 'googleCloud', 'locationIQ']
    idx = 0
    blank = True
    while idx < len(arr):
        if arr[idx] in request.form and request.form[arr[idx]] != "":
            command = "UPDATE apiKeys SET {} = \"{}\" WHERE id = {};"
            c.execute(command.format(arr[idx],request.form[arr[idx]],userID))
            blank = False
            db.commit()
        idx += 1
    if not blank:
        if button == 'Update Key':
            flash("Key Updated Successfully!")
        else:
            flash("Key Added Successfully!")
    else:
        flash("No Key Added")
    db.commit()
    db.close()

def getAPIKey(api): #@param api is which api key to retrieve from the database
    key = ''
    dbfile = "data.db"
    db = sqlite3.connect(dbfile)
    c = db.cursor()
    q = c.execute("SELECT {} FROM apiKeys WHERE id = {};".format(api,userID))
    for bar in q:
        key = bar[0]
    return key
