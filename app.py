from flask import Flask, url_for, render_template, request, redirect
from markupsafe import escape

from models import *

app = Flask(__name__)

@app.get("/login/")
def login_get():
    return render_template("login.html")

@app.post("/login/")
def login_post():
    username = request.form['username']
    password = request.form['password']
    # Jika login tidak valid
    if Player.query.filter((Player.username == username) & (Player.password == password)).first() == None:
        return redirect(url_for('login_get'))

    return redirect(url_for('index'))

@app.get("/register/")
def register_get():
    return render_template("register.html")

@app.post("/register/")
def register_post():
    username = request.form['username']
    password = request.form['password']
    # Jika username sudah digunakan
    if Player.query.filter(Player.username == username).first() != None:
        return redirect(url_for('register_get'))
    
    player = Player(
        username=username,
        password=password,
        is_online=1
    )

    db_session.add(player)
    db_session.commit()

    return redirect(url_for('index'))

@app.route("/")
def index():
    return "<p>Index Page!</p>"

@app.route("/user/<username>")
def profile(username):
    return f"<p>profil {escape(username)}</p>"

# with app.test_request_context():
#     print(url_for('login'))
#     print(url_for('index'))
#     print(url_for('profile', username="Egi Putra Ragil"))