from flask import Flask, send_from_directory, request, url_for
from database import Database
import password_manager
app = Flask(__name__)

@app.before_first_request
def startup():
    password_manager.initialize()
    
@app.route("/")
def hello():
    return app.send_static_file('home.html')

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file("login.html")
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

@app.route("/create_acc",methods = ['GET','POST'])
def create_account():
    if request.method == 'GET':
            return app.send_static_file("create_account.html")
    if request.method == 'POST':
        if not request.form['password'] == request.form['confirm_password']:
            return "Password Not Matching"
        else:
            password_manager.create_account(request.form['username'],request.form['password'])
            return "success"
    else:
        return "Error"