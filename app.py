from flask import Flask, url_for, render_template
from markupsafe import escape

from models import *

app = Flask(__name__)

@app.get("/login/")
def login():
    return render_template("login.html")

@app.post("/login/")
def login():
    
    return render_template("login.html")

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route("/")
def index():
    return "<p>Index Page!</p>"

@app.route("/user/<username>")
def profile(username):
    return f"<p>profil {escape(username)}</p>"

with app.test_request_context():
    print(url_for('login'))
    print(url_for('index'))
    print(url_for('profile', username="Egi Putra Ragil"))