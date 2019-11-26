#Team NSA_Advice
#huangT, linW, sontagC, zenH
#SoftDev1 pd2
#P #01: ArRESTed Development
#2019-11-2-

from flask import Flask, render_template, request,  session, redirect, url_for, flash
import sqlite3
import urllib, json
import api
app = Flask(__name__)
app = Flask(__name__)
app.secret_key = "adsfgt"

session = {}
userInfo = {}
userID = -1

@app.route("/")
def root():
    if 'user' in session:
        return redirect(url_for("home"))
    else:
        #flash(api.getIP()) #Coby debug statement
        return render_template("index.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
    return render_template("register.html")

@app.route("/update", methods = ["POST", "GET"])
def update():
    return render_template("update.html")

@app.route("/auth", methods = ["POST"])
def auth():
    global userID
    if request.form['submit_button'] == "Sign me up":
        if request.form['password'] != request.form['password2']:
            flash("Error! Passwords do not match")
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
                    return redirect(url_for("register"))
                else:
                    id = getTableLen("users") #gives the user the next availabe id
                    c.execute("INSERT INTO users VALUES(?, ?, ?);", (id, request.form['username'], request.form['password'])) #different version of format
                    c.execute("INSERT INTO info VALUES(?, ?, ?, ?, ?, ?)", (id, request.form['firstName'], request.form['lastName'], request.form['email'], str(request.form['phoneNum']), ""))
                    db.commit()
                    db.close()
                    flash("Register Success!")
                    flash("index")
                    return redirect(url_for("home"))
    if request.form['submit_button'] == "Login":
        dbfile = "data.db"
        db = sqlite3.connect(dbfile)
        c = db.cursor() #above three lines allow sqlite commands to be performed from python script
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
                    return redirect(url_for("home"))
                else:
                    flash("Error! Incorrect password")
                    return redirect(url_for("login"))
        else:
            flash("Error! Incorrect username")
            return redirect(url_for("login"))
    if request.form['submit_button'] == "Update Info":
        dbfile = "data.db"
        db = sqlite3.connect(dbfile)
        c = db.cursor() #above three lines allow sqlite commands to be performed from python script
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
        db.close()
        return redirect(url_for("home"))

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
        userID = -1
    flash("Logout Success!")
    flash("index")
    return redirect(url_for("root"))

@app.route("/home")
def home(): #display home page of website
    if 'user' in session:
        fillUserInfo()
        return render_template(
            "homepage.html",
            #google_key = session['google_key'],
            user = session['user'],
            name = userInfo['firstName'] + " " + userInfo['lastName'],
            email = userInfo['email'],
            pnum = userInfo['phoneNum'],
            loc = userInfo['location'])
    else:
        return redirect(url_for("root"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/howToUse")
def howToUse():
    return render_template("howToUse.html")

@app.route("/weather")
def weather():
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=da19d101a993403bd4ab9a3284ec0f0d"
    if userInfo['location'] != "":
        loc = userInfo['location']
        if ' ' in loc:
            loc = loc.replace(' ', '%20')
        try:
            u = urllib.request.urlopen(url.format(loc))
            response = u.read()
            data = json.loads(response)
            return render_template("weather.html", info = data)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                flash("Error! Invalid city name")
                return redirect(url_for("home"))
            else:
                flash("Not 404 error.")
                return redirect(url_for("home"))
    else:
        flash("Location required. Please enter a city name.")
        return redirect(url_for("home"))


def getTableLen(tbl): #returns the length of a table
    dbfile = "data.db"
    db = sqlite3.connect(dbfile)
    c = db.cursor()
    command = "SELECT COUNT(*) FROM {};"
    q = c.execute(command.format(tbl))
    for line in q:
        return line[0]

def fillUserInfo():
    dbfile = "data.db"
    db = sqlite3.connect(dbfile)
    c = db.cursor()
    q = c.execute("SELECT * FROM info WHERE id = {}".format(userID))
    for bar in q:
        userInfo['firstName'] = bar[1]
        userInfo['lastName'] = bar[2]
        userInfo['email'] = bar[3]
        userInfo['phoneNum'] = bar[4]
        userInfo['location'] = bar[5]

if __name__ == "__main__":
    app.debug = True
    app.run()
