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

@app.route("/login", methods = ["POST"])
def login():
    return render_template("login.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
    return render_template("register.html")

@app.route("/auth", methods = ["POST"])
def auth():
    if request.form['signup_submit'] == "Sign me up":
        if (request.form['username'] == "" or request.form['password'] == "" or request.form['password2'] == ""): #return error if username or password is empty
            flash("ERROR! One or more fields cannot be blank")
            flash("invalid error")
            return redirect(url_for("register"))
        elif request.form['password'] != request.form['password2']:
            flash("ERROR! Passwords do not match")
            flash("invalid error")
            return redirect(url_for("register"))
            return 0

@app.route("/home")
def home(): #display home page of website
    if 'user' in session:
        return render_template("homepage.html")
    else:
        return redirect(url_for("root"))

if __name__ == "__main__":
    app.debug = True
    app.run()
