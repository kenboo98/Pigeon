from flask import Flask, send_from_directory, request, url_for
from database import Database
app = Flask(__name__)

@app.before_first_request
def startup():
    global db
    db = Database("message_list")
    print("database tables created")

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/comment_portal", methods = ['GET','POST'])
def comment_portal():
    if request.method == 'GET':
        return app.send_static_file("index.html")
    if request.method == 'POST':
        db.store_message(request.form['comment'])
        return request.form['comment']
    else:
        return "error"
