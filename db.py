from flask import Flask, render_template, request,  session, redirect, url_for, flash
import sqlite3 # enable control of an sqlite database

db=0

def init():
    dbfile = "data.db"
    db = sqlite3.connect(dbfile)
    c = db.cursor()

def exit():
    db.commit()
    db.close()

def example():
    c = init()
    c.execute('whatever')
    exit()

#---------------------------------

def addUser():
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
            if bar[0] > 0:
                flash("Username is already taken. Please choose another one.")
                return False
            else:
                id = getTableLen("users") #gives the user the next availabe id
                c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (id, request.form['username'], request.form['password'], request.form['firstName'], request.form['lastName'], request.form['email'], str(request.form['phoneNum']), "")) #different version of format
                db.commit()
                db.close()
                flash("Register Success!")
                flash("index") #Why flash index?
                return True
        if bar[0] > 0:
            flash("Username is already taken. Please choose another one.")
            return False
        else:
            id = getTableLen("users") #gives the user the next availabe id
            c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (id, request.form['username'], request.form['password'], request.form['firstName'], request.form['lastName'], request.form['email'], str(request.form['phoneNum']), "", "")) #different version of format
            db.commit()
            db.close()
            flash("Register Success!")
            flash("index") #Why flash index?
            return True

def login():
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
            if request.form['password'] == p[0]: #correct username and password
                session['user'] = request.form['username'] #stores the user in the session
                userID = bar[0][1][0]
                f = open("keys.txt", "r") #opens file with the keys
                keys = f.readlines()
                k = keys[0].split(":")
                #print(k)
                #print(k[1].strip())
                session['google_key'] = k[1].strip()
                fillUserInfo()
                return True
            else:
                flash("Error! Incorrect password")
                return False
    else:
        flash("Error! Incorrect username")
        return False

def update():
    dbfile = "data.db"
    db = sqlite3.connect(dbfile)
    c = db.cursor()c = db.cursor()
    blank = True
    arr = ['firstName','lastName','username','password','email','phoneNum','location']
    idx = 0
    while idx < len(arr):
        if arr[idx] == 'username' or arr[idx] == 'password':
            if request.form[arr[idx]] != "":
                command = "UPDATE users SET \"{}\" = \"{}\" WHERE id = {};"
                c.execute(command.format(arr[idx],request.form[arr[idx]],userID))
                session['user'] = request.form['username']
                blank = False
                db.commit()
        else:
            if request.form[arr[idx]] != "":
                command = "UPDATE info SET \"{}\" = \"{}\" WHERE id = {};"
                c.execute(command.format(arr[idx],request.form[arr[idx]],userID))
                blank = False
                db.commit()
        idx += 1
    if not blank:
        flash("Update Success!")
    else:
        flash("Nothing has been updated.")
    fillUserInfo()
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
