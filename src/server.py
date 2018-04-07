from flask import session, Flask, send_from_directory, request, url_for, redirect
from flask_socketio import SocketIO
from database import UserDB

app = Flask(__name__, static_folder='../static')
app.config['SECRET_KEY'] = 'PIGEON'
socketio = SocketIO(app)

@app.before_first_request
def init():
    # initialize user database for login and signup
    global User
    User = UserDB()

@app.route("/")
def home():
    # route to home
    if 'name' in session:
        return redirect(url_for('chat'))
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
            session['name'] = request.form['username']
            return redirect(url_for('chat'))
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

@app.route("/chat")
def chat():
    name = session.get('name', '')
    return app.send_static_file("chat.html")

@socketio.on('message', namespace='/chat')
def message_recv(message):
    data = messgage['data']
    data.author = session.get('name')
    emit('message', {'data': data}, broadcast = True)

@socketio.on('joined', namespace='/chat')
def joined(message):
    emit('status', {'message': session.get('name') + ' has entered Pigeon chat.'})

@socketio.on('left', namespace='/chat')
def left(message):
    session.pop('name', None)
    emit('status', {'messsage': session.get('name') + ' has left Pigeon Chat'})
    return redirect(url_for('home'))

if __name__ == "__main__":
    socketio.run(app)
