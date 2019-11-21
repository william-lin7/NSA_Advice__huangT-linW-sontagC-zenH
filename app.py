#Team NSA_Advice
#huangT, linW, sontagC, zenH
#SoftDev1 pd2
#P #01: ArRESTed Development
#2019-11-2-

from flask import Flask, render_template
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

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
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
