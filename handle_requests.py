from flask import Flask, send_from_directory, request, url_for

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/comment_portal", methods = ['GET','POST'])
def comment_portal():
    if request.method == 'GET':
        return app.send_static_file("index.html")
    if request.method == 'POST':
        return request.form['comment']
    else:
        return "error"
