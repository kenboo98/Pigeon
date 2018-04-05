from flask import Flask, send_from_directory, request, url_for, redirect
from database import UserDB

app = Flask(__name__, static_folder='../static')

@app.before_first_request
def init():
    # initialize user database for login and signup
    global User
    User = UserDB()

@app.route("/")
def home():
    # route to home
    return app.send_static_file('index.html')

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file("login.html")
    if request.method == 'POST':
        # verifies user info and logs them into our server
        result = User.verify_login(request.form['username'], request.form['password'])
        if (result == 102):
            # login user and display chat
            return "Welcome " + request.form['username']
        elif (result == 431):
            # If user enters wrong username or password
            return "Error: Wrong Username or Password, please try again"
    else:
        # uncaught errors
        return "Error"

@app.route("/signup", methods = ['GET','POST'])
def new_account():
    if request.method == 'GET':
            return app.send_static_file("signup.html")
    if request.method == 'POST':
        if not request.form['password'] == request.form['confirm_password']:
            return "Error: Passwords did not match, please try again"
        else:
            result = User.create_account(request.form['username'], request.form['password'])
            if result == 101:
                # this is where we would log the user
                return redirect(url_for('login'))
            elif result == 421:
                # user ID already in database
                return "Email already registered with Pigeon, please login or try\
                        a different email"
    else:
        return "Error"

if __name__ == "__main__":
    app.run()
