#Team NSA_Advice
#huangT, linW, sontagC, zenH
#SoftDev1 pd2
#P #01: ArRESTed Development
#2019-11-2-

from flask import Flask, render_template, request,  session, redirect, url_for, flash
import sqlite3
import urllib, json
import api
import db as dbase
app = Flask(__name__)
app = Flask(__name__)
app.secret_key = "adsfgt"

session = {}
userInfo = {}
db = 0

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
    if request.form['submit_button'] == "Sign me up":
        if dbase.addUser():
            return redirect(url_for("root"))
        else:
            return redirect(url_for("register"))
    if request.form['submit_button'] == "Login":
        if dbase.login():
            session['user'] = request.form['username'] #stores the user in the session
            f = open("keys.txt", "r") #opens file with the keys
            keys = f.readlines()
            k = keys[0].split(":")
            #print(k)
            #print(k[1].strip())
            session['google_key'] = k[1].strip()
            dbase.fillUserInfo(userInfo)
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))
    if request.form['submit_button'] == "Update Info":
        dbase.update()
        dbase.fillUserInfo(userInfo)
        return redirect(url_for("home"))

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
        dbase.userID = -1
    flash("Logout Success!")
    flash("index")
    return redirect(url_for("root"))

@app.route("/home")
def home(): #display home page of website
    if 'user' in session:
        dbase.fillUserInfo(userInfo)
        return render_template(
            "homepage.html",
            google_key = session['google_key'],
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
            return render_template("weather.html",
                                    info = data,
                                    weather = data["weather"][0]["main"],
                                    temp = format((data["main"]["temp"] - 273) * (9/5) + 32, ".1f"),
                                    description = data["weather"][0]["description"],
                                    wind = data["wind"]["speed"],
                                    pressure = data["main"]["pressure"],
                                    humidity = data["main"]["pressure"]
                                    )
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

@app.route("/civicInfo")
def civicInfo():
    #Address Format:
    #345%20Chamber%20St.%20NewYork%20City%20NY
    urlelections: "https://www.googleapis.com/civicinfo/v2/elections?key=AIzaSyCk3JsYEm11AV1n2fGD7CPJ08Z34oRG1Hc&address={}"
    urlvoterinfo = "https://www.googleapis.com/civicinfo/v2/voterinfo?key=AIzaSyCk3JsYEm11AV1n2fGD7CPJ08Z34oRG1Hc&address={}&electionId={}}"
    if userInfo['address'] != "":
        addr = userInfo['address']
        if ' ' in addr:
            addr = loc.replace(' ', '%20')
        try:
            u1 = urllib.request.urlopen(urlelections.format(addr))
            response1 = u.read()
            data1 = json.loads(response1)
            elections = data1["elections"]
            id = []
            name = []
            for election in elections:
                id.append(election["id"])
                name.append(election["name"])
            vinfo = []
            for elecid in id:
                u2 = urllib.request.urlopen(urlvoterinfo.format(addr, elecid))
                response2 = u.read()
                data2 = json.loads(response2)
                vinfo.append(data2)
            return render_template("civicInfo.html",
                            name = name,
                            vinfo = vinfo)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                flash("Error! Invalid address")
                return redirect(url_for("home"))
            else:
                flash("Not 404 error.")
                return redirect(url_for("home"))
    else:
        flash("Address required. Please enter an address.")
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()
