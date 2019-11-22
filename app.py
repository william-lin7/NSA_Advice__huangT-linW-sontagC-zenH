#Team NSA_Advice
#huangT, linW, sontagC, zenH
#SoftDev1 pd2
#P #01: ArRESTed Development
#2019-11-2-

from flask import Flask, render_template, request,  session, redirect, url_for, flash
import sqlite3
import urllib, json
app = Flask(__name__)
app = Flask(__name__)
app.secret_key = "adsfgt"

session = {}

@app.route("/")
def root():
    if 'user' in session:
        return redirect(url_for("home"))
    else:
        return render_template("index.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
    return render_template("register.html")

@app.route("/auth", methods = ["POST"])
def auth():
    if request.form['submit_button'] == "Sign me up":
        if (request.form['username'] == "" or request.form['password'] == "" or request.form['password2'] == ""): #return error if username or password is empty
            flash("Error! One or more fields cannot be blank")
            flash("invalid error")
            return redirect(url_for("register"))
        elif request.form['password'] != request.form['password2']:
            flash("Error! Passwords do not match")
            flash("invalid error")
            return redirect(url_for("register"))
        else:
            dbfile = "data.db"
            db = sqlite3.connect(dbfile)
            c = db.cursor() #standard connection
            command = "SELECT COUNT(*) FROM users WHERE username = \"{}\";"
            newUser = c.execute(command.format(request.form['username'])) #execution of sqlite command with the given username instead of the brackets
            for bar in newUser:
                if bar[0] > 0:
                    flash("Username is already taken. Please choose another one.")
                    flash("register error")
                    return redirect(url_for("register"))
                else:
                    id = getTableLen("users") #gives the user the next availabe id
                    c.execute("INSERT INTO users VALUES(?, ?, ?);", (id, request.form['username'], request.form['password'])) #different version of format
                    db.commit()
                    db.close()
                    flash("Register Success!")
                    return redirect(url_for("home"))
    if request.form['submit_button'] == "Login":
        if (request.form['username'] == "" or request.form['password'] == ""): #return error if username or password is empty
            flash("ERROR! One or more fields cannot be blank")
            flash("invalid error")
            return redirect(url_for("login"))
        else:
            dbfile = "data.db"
            db = sqlite3.connect(dbfile)
            c = db.cursor() #above three lines allow sqlite commands to be performed from python script
            command = "SELECT username FROM users WHERE username = \"{}\";"
            listUsers = c.execute(command.format(request.form['username'])) #fills in brackets with the given username and executes it in sqlite
            bar = list(enumerate(listUsers))
            if len(bar) > 0: #checks whether there exists a user with the given username
                getPass = "SELECT password FROM users WHERE username = \"{}\";"
                listPass = c.execute(getPass.format(bar[0][1][0]))
                for p in listPass:
                    if request.form['password'] == p[0]: #correct username and password
                        session['user'] = request.form['username'] #stores the user in the session
                        f = open("keys.txt", "r") #opens file with the keys
                        keys = f.readlines()
                        k = keys[0].split(":")
                        #print(k)
                        #print(k[1].strip())
                        session['google_key'] = k[1].strip()
                        return redirect(url_for("home"))
                    else:
                        flash("Error! Incorrect password")
                        flash("invalid error")
                        return redirect(url_for("login"))
            else:
                flash("Error! Incorrect username")
                flash("invalid error")
                return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop('user')
    flash("Logout Success!")
    return redirect(url_for("root"))

@app.route("/home")
def home(): #display home page of website
    if 'user' in session:
        return render_template("homepage.html", google_key = session['google_key'])
    else:
        return redirect(url_for("root"))

def getTableLen(tbl): #returns the length of a table
    dbfile = "data.db"
    db = sqlite3.connect(dbfile)
    c = db.cursor()
    command = "SELECT COUNT(*) FROM {};"
    q = c.execute(command.format(tbl))
    for line in q:
        return line[0]

if __name__ == "__main__":
    app.debug = True
    app.run()
