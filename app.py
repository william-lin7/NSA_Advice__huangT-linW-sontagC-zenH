#Team NSA_Advice
#huangT, linW, sontagC, zenH
#SoftDev1 pd2
#P #01: ArRESTed Development
#2019-11-2-

from flask import Flask, render_template, request,  session, redirect, url_for, flash
import sqlite3
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

@app.route("/auth", methods = ["POST"])
def auth():
    print(request.form)
    if (request.form['submit_button'] == 'Login'):
        return render_template("login.html")
    elif (request.form['submit_button'] == 'Register'):
        return render_template("register.html")

@app.route("/home")
def home(): #display home page of website
    if 'user' in session:
        return render_template("homepage.html")
    else:
        return redirect(url_for("root"))

if __name__ == "__main__":
    app.debug = True
    app.run()
