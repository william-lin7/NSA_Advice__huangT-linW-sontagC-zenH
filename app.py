#Team NSA_Advice
#huangT, linW, sontagC, zenH
#SoftDev1 pd2
#P #01: ArRESTed Development
#2019-11-2-

from flask import Flask, render_template, request,  session, redirect, url_for, flash
import sqlite3
import urllib, json
import api #helper functions found in api.py
import db as dbase  #helper functions found in db.py
app = Flask(__name__)
app = Flask(__name__)
app.secret_key = "adsfgt"

session = {}
userInfo = {}

@app.route("/") #Initally loaded page
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

@app.route("/update", methods = ["POST", "GET"]) #The page accessed to update your own data
def update():
    return render_template("update.html")

@app.route("/auth", methods = ["POST"]) #This route authenticates registration and log in, and other updates
def auth():
    if request.form['submit_button'] == "Sign me up": #If you were sent here by registering
        if dbase.addUser(): #@tyler when is user added to session? #adds user data to our db
            return redirect(url_for("root"))
        else:
            return redirect(url_for("register")) #if addUser() returns false, it will also handle flashing the correct error message
    if request.form['submit_button'] == "Login": #if sent here by lgging in
        if dbase.login():
            session['user'] = request.form['username'] #stores the user in the session
            dbase.fillUserInfo(userInfo) #gives easy access to user information via userInfo variable
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))
    if request.form['submit_button'] == "Update Info": #If updating info, fill in db
        dbase.update()
        dbase.fillUserInfo(userInfo) #gives easy access to user information via userInfo variable
        return redirect(url_for("home"))
    if request.form['submit_button'] == "Update Key" or request.form['submit_button'] == "Add Key":
        dbase.updateAPIKey(request.form['submit_button'])
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
        dbase.fillUserInfo(userInfo) #grabs user info
        key = dbase.getAPIKey('locationIQ')
        url = "https://us1.locationiq.com/v1/search.php?key={}&q={}&format=json"
        lat = 0
        lon = 0
        plc = ['atm','bakery','bank','bus_station','cafe','church','clothing_store','gym','hospital','laundry','library','school','supermarket','train_station','park']
        if userInfo['address'] != "":
            addr = userInfo['address']
            if ' ' in addr:
                addr = addr.replace(' ', '%20')
            try:
                u = urllib.request.urlopen(url.format(key,addr))
                response = u.read()
                data = json.loads(response)
                lat = data[0]["lat"]
                lon = data[0]["lon"]
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    flash("Error! Invalid Address. Map unavailable.")
                elif e.code == 401:
                    flash("Error! Invalid API Key. Map unavailable.")
                else:
                    flash("Error! Map unavailable.")
        else:
            flash("Address required for map. Please enter an address")
        return render_template(
            "homepage.html",
            googleCivic = dbase.getAPIKey("googleCivic"),
            openWeather = dbase.getAPIKey("openWeather"),
            mapskey = dbase.getAPIKey('googleMaps'),
            user = userInfo['username'],
            name = userInfo['firstName'] + " " + userInfo['lastName'],
            loc = userInfo['location'],
            address = userInfo['address'],#fills out page with all of a users info
            lat = lat,
            lon = lon,
            places = plc)
    else:
        return redirect(url_for("root"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/howToUse")
def howToUse():
    return render_template("howToUse.html")

@app.route("/weather") #renders a separate page with weather data for a user
def weather():
    key = dbase.getAPIKey('openWeather')
    if key == "":
        flash("Error! Missing API Key")
        return redirect(url_for("home"))
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}"
    if userInfo['location'] != "":
        loc = userInfo['location']
        if ' ' in loc:
            loc = loc.replace(' ', '%20')
        try:
            u = urllib.request.urlopen(url.format(loc,key))
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
                flash("Error! Invalid City Name")
                return redirect(url_for("home"))
            elif e.code == 401:
                flash("Error! Invalid API Key")
                return redirect(url_for("home"))
            else:
                flash("Error!")
                return redirect(url_for("home"))
    else:
        flash("Location required. Please enter a city name.")
        return redirect(url_for("home"))

@app.route("/elections") #renders separate page with election (local) data
def elections():
    key = dbase.getAPIKey('googleCivic')
    #Address Format:
    #345%20Chamber%20St.%20NewYork%20City%20NY
    urlelections = "https://www.googleapis.com/civicinfo/v2/elections?key={}&address={}"
    urlvoterinfo = "https://www.googleapis.com/civicinfo/v2/voterinfo?key={}&address={}&electionId={}"
    if userInfo['address'] != "":
        addr = userInfo['address']
        if ' ' in addr:
            addr = addr.replace(' ', '%20')
        try:
            u1 = urllib.request.urlopen(urlelections.format(key,addr))
            response1 = u1.read()
            data1 = json.loads(response1)
            elections = data1["elections"]
            id = []
            name = []
            for election in elections:
                id.append(election["id"])
                name.append(election["name"])
            vinfo = []
            for elecid in id:
                u2 = urllib.request.urlopen(urlvoterinfo.format(key,addr, elecid))
                response2 = u2.read()
                data2 = json.loads(response2)
                vinfo.append(data2)
            return render_template("elections.html",
                            name = name,
                            vinfo = vinfo)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                flash("Error! Invalid Address")
                return redirect(url_for("home"))
            elif e.code == 401:
                flash("Error! Invalid API Key")
                return redirect(url_for("home"))
            else:
                flash("Error!")
                return redirect(url_for("home"))
    else:
        flash("Address required. Please enter an address")
        return redirect(url_for("home"))

@app.route("/representatives") #separate page with political officials
def representatives():
    key = dbase.getAPIKey('googleCivic')
    if key == "":
        flash("Error! Missing API Key")
        return redirect(url_for(root))
    url = "https://www.googleapis.com/civicinfo/v2/representatives?key={}&address={}"
    if userInfo['address'] != "":
        addr = userInfo['address']
        if ' ' in addr:
            addr = addr.replace(' ', '%20')
        try:
            u = urllib.request.urlopen(url.format(key,addr))
            response = u.read()
            data = json.loads(response)
            return render_template("representatives.html",
                                    reps = data["officials"])
        except urllib.error.HTTPError as e:
            if e.code == 404:
                flash("Error! Invalid Address")
                return redirect(url_for("home"))
            elif e.code == 401:
                flash("Error! Invalid API Key")
                return redirect(url_for("home"))
            else:
                flash("Error!")
                return redirect(url_for("home"))
    else:
        flash("Address required. Please enter an address")
        return redirect(url_for("home"))


@app.route("/places/<plc>")
def places(plc):
    key = dbase.getAPIKey('locationIQ')
    #key2 = dbase.getAPIKey('googleCivic')
    key2 = "AIzaSyA4Rb84cl3x6kVw6AZuPrhQgP9teGyPN6A"
    if key == "":
        flash("Error! Missing API Key")
        return redirect(url_for("root"))
    url = "https://us1.locationiq.com/v1/search.php?key={}&q={}&format=json"
    url2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}&radius={}&type={}&key={}"
    if userInfo['address'] != "":
        addr = userInfo['address']
        if ' ' in addr:
            addr = addr.replace(' ', '%20')
        try:
            u = urllib.request.urlopen(url.format(key,addr))
            response = u.read()
            data = json.loads(response)
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            u2 = urllib.request.urlopen(url2.format(lat + ',' + lon, 1500, plc, key2))
            response2 = u2.read()
            data2 = json.loads(response2)
            return render_template("places.html",
                                    info = data2["results"])
        except urllib.error.HTTPError as e:
            if e.code == 404:
                flash("Error! Invalid Address")
                return redirect(url_for("home"))
            elif e.code == 401:
                flash("Error! Invalid API Key")
                return redirect(url_for("home"))
            else:
                flash("Error!")
                return redirect(url_for("home"))
    else:
        flash("Address required. Please enter an address")
        return redirect(url_for("home"))

@app.route("/keys")
def keys():
    print(dbase.getAPIKey('googleMaps'))
    if 'user' in session:
        return render_template("keys.html",
                                owkey = dbase.getAPIKey('openWeather'),
                                gckey = dbase.getAPIKey('googleCivic'),
                                lqkey = dbase.getAPIKey('locationiq'),
                                gmkey = dbase.getAPIKey('googleMaps'))
    else:
        return redirect(url_for("root"))


if __name__ == "__main__":
    app.debug = True
    app.run()
