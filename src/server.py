from flask import Flask, send_from_directory, request, url_for
from database import Database
import passwords

app = Flask(__name__)

@app.before_first_request
def startup():
    password_manager.initialize()

@app.route("/")
def home():
    return app.send_static_file('../static/home.html')

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file("../static/login.html")
    if request.method == 'POST':
        result = password_manager.verify_login(request.form['username'],request.form['password'])
        if(result == "keyerror"):
            return "KEYERROR"
        if(result == True):
            return "Welcome " + request.form['username']
        else:
            return "Wrong Password or Username"

    else:
        return "error"

@app.route("/new",methods = ['GET','POST'])
def new_account():
    if request.method == 'GET':
            return app.send_static_file("../static/new_account.html")
    if request.method == 'POST':
        if not request.form['password'] == request.form['confirm_password']:
            return "Password Not Matching"
        else:
            password_manager.create_account(request.form['username'],request.form['password'])
            return "success"
    else:
        return "Error"
