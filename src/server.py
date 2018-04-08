from flask import session, Flask
from flask import render_template, send_from_directory, request, url_for, redirect
from flask_socketio import SocketIO, emit, send
from database import UserDB, PostsDB
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PIGEON'
socketio = SocketIO(app)

@app.before_first_request
def init():
    # initialize user database for login and signup
    global Users
    global Posts
    Users = UserDB()
    Posts = PostsDB()

@app.route("/")
def home():
    # redirect to chat if user already logged in
    if 'username' in session:
        return redirect(url_for('chat'))
    # route to home
    return render_template('index.html')

@app.route("/login", methods = ['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('chat'))
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        # verifies user info and logs them into our server
        result = Users.verify_login(request.form['username'], request.form['password'])
        if (result == 102):
            # login user and display chat
            session['username'] = request.form['username']
            session['lastLoaded'] = Posts.getCount() + 1
            return redirect(url_for('chat'))
        elif (result == 431):
            # If user enters wrong username or password
            return "Error: Wrong Username or Password, please try again"
    else:
        # uncaught errors
        return "Error"

@app.route("/signup", methods = ['GET','POST'])
def new_account():
    if 'username' in session:
        return redirect(url_for('chat'))
    if request.method == 'GET':
            return render_template("signup.html")
    if request.method == 'POST':
        if not request.form['password'] == request.form['confirm_password']:
            return "Error: Passwords did not match, please try again"
        else:
            result = Users.create_account(request.form['username'], request.form['password'])
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
    username = session.get('username', '')
    return render_template("chat.html")

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('home'))

@socketio.on('message', namespace='/chat')
def message_recv(message):
    data = message['data']
    data['author'] = session.get('username')
    data['timestamp'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M")
    new_post(session.get('username'), data['message'], data['timestamp'])
    emit('message', {'data': data}, broadcast = True)

@socketio.on('joined', namespace='/chat')
def joined(message):
    data = {}
    data['message'] = session.get('username') + ' has entered Pigeon chat.'
    data['timestamp'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M")
    emit('status', {'data': data}, broadcast = True)

@socketio.on('left', namespace='/chat')
def left(message):
    data = {}
    data['message'] = session.get('username') + ' has left Pigeon chat.'
    data['timestamp'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M")
    emit('status', {'data': data}, broadcast = True)

@socketio.on('loadUp', namespace='/chat')
def loadUp(_):
    data = {}
    prev_posts, session['lastLoaded'] = get_prev_posts(10, session.get('lastLoaded'))
    data['messages'] = prev_posts
    data['count'] = len(prev_posts)
    emit('previous', {'data': data}, broadcast = False)

# socketio annotation doesn't see global posts var
def new_post(u_id, msg, tstamp):
    Posts.addPost(u_id, msg, tstamp)

def get_prev_posts(count, lastLoaded):
    return Posts.loadLast(count, lastLoaded)

if __name__ == "__main__":
    socketio.run(app)
