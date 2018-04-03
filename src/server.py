from flask import Flask, send_from_directory, request, url_for
from database import Database
import password_manager

app = Flask(__name__)

@app.before_first_request
def startup():
    password_manager.initialize()

@app.route("/")
def home():
    return app.send_static_file('../static/index.html')

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file("../static/login.html")
    if request.method == 'POST':
        result = password_manager.verify_login(request.form['username'],request.form['password'])
        if (result == "KeyError"):
            return "Error: Not a valid password form, please try again"
        if (result == True):
            return "Welcome " + request.form['username']
        else:
            return "Error: Wrong Username or Password, please try again"
    else:
        return "error"

@app.route("/new",methods = ['GET','POST'])
def new_account():
    if request.method == 'GET':
            return app.send_static_file("../static/signup.html")
    if request.method == 'POST':
        if not request.form['password'] == request.form['confirm_password']:
            return "Error: Passwords did not match, please try again"
        else:
            password_manager.create_account(request.form['username'],request.form['password'])
            return "success"
    else:
        return "Error"
