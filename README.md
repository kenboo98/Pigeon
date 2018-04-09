<p align="center"><img src="https://github.com/dandua98/Pigeon/blob/master/common/images/logo.png" width="400"></br></p>

# Pigeon
A chat web app made with Flask, SocketsIO and MongoDB for CMPUT 275 final project, with @kenboo98</br>
Involves our own implementation of SHA256

## Idea and Execution
The basic idea behind the application was to make a chat application using Web Sockets and we had to use python somewhere in the project since course restrictions so we use Flask for our backend. We decided to implement SHA256 hashing ourselves too since it didn't really look that bad (kudos to NIST for the amazing standards [publication](https://csrc.nist.gov/csrc/media/publications/fips/180/4/final/documents/fips180-4-draft-aug2014.pdf)). We used MongoDB for our database to store user data and posts. I would prefer using MySQL if we add rooms and other features (relational database would be amazing for that) later on but since we were short on time, we sticked with something fast and easy.</br>
<p align="center"><img src="https://github.com/dandua98/Pigeon/blob/master/common/images/chat.png" width="750"></p></br>

## Getting Started
This would help you setup our environment on your own system for development and testing. Feel free to fork and make a pull request if you want to contribute to our project.

### Prerequisites
The backend was created using following libraries:
* Flask
* SocketIO (Flask_SocketIO)
* MongoDB (pymongo)

These can be installed using pip or simply with our [requirements](https://github.com/dandua98/Pigeon/blob/master/requirements.txt) file using pip:
```sh
$ pip install -r requirements.txt # python2
    # or
$ pip3 intall -r requirements.txt # python3  
```

Documentation for the modules can be found here:
* [Flask](http://flask.pocoo.org/docs/0.12/)
* [Flask_SocketIO](https://flask-socketio.readthedocs.io/en/latest/)
* [pymongo](https://api.mongodb.com/python/current/)

We used Flask sessions to store users logged in on server, more information can be found [here](https://pythonhosted.org/Flask-Session/).

#### MongoDB setup
You will need to make a new Database and initialize the corresponding documents for PIGEON database. This is a very simple process and can be done from mongo shell. First, you will need to run the mongo daemon.
```sh
$ cd Pigeon
$ mongod
```

Then, in another shell, launch the mongo shell and run the following commands
```sh
$ cd Pigeon
$ mongod

$ use PIGEON
$ db.createCollection("users", {autoIndexId:true})
$ db.users.insert({"u_id":"root@root.com", "password":"4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2"})
$ db.createCollection("posts")
$ db.posts.insert({"_id":1, "u_id":"root@root.com", "post":"Welcome to Pigeon Chat!", "timestamp":"18-04-07 15:11"})
```
This creates a new Database called PIEGON and adds two documents, users and posts to the database. These need to be initialized so you need to insert something in the documents initially, we just added a test user and a simple message.

### Installation
To install and run, in your command line/terminal tool, run:
```sh
$ git clone https://github.com/dandua98/Pigeon.git
$ cd Pigeon
$ python3 server.py
```

_Assumes required packages have been installed_

In another terminal, run the MongoDB server
```sh
$ cd Pigeon
$ mongod
```

Now, in a web browser, launch localhost on port 5000, or click on http://127.0.0.0:5000

## Usage
<p align="center"><img src="https://github.com/dandua98/Pigeon/blob/master/common/images/main.png" width="600" height= "400"></p><br/>
* Main Screen - Index screen for Pigeon chat service, click login for returning user, sign up for new user<br/>

<p align = "center"><img src="https://github.com/dandua98/Pigeon/blob/master/common/images/login.png"  height=225px style="margin-right: 10px; width: 50%"> <img src="https://github.com/dandua98/Pigeon/blob/master/common/images/signup.png" height = 225px style="margin-left: 10px; width: 50%"></p> <br/>
* Login screen - To login for a current user and sign up for a new user, additional data like weight and height can later be used for health data<br/>

<p align="center"><img src="https://github.com/dandua98/Pigeon/blob/master/common/images/chat.png" width="500"></p><br/>
* Chat screen - Enter new messages and load previous messages using the button on top right of chat panel<br/>

## Authors
* __Danish Dua__ - _Software engineering student at University of Alberta_ - [GitHub](https://github.com/dandua98)
* __Kenta Tellambura__ - _Software engineering student at University of Alberta_ - [GitHub](https://github.com/kenboo98)

## License
The project is licensed under MIT License - see the [LICENSE](https://github.com/dandua98/Pigeon/blob/master/LICENSE "LICENSE") file for details

## Acknowledgement
* Any open source codebase that way used in this project
* NIST (National institute of standards and technology) [publication](https://csrc.nist.gov/csrc/media/publications/fips/180/4/final/documents/fips180-4-draft-aug2014.pdf) for SHA standards
* [CMPUT 275](https://www.ualberta.ca/computing-science/undergraduate-studies/course-directory/courses/introduction-to-tangible-computing-ii) Winter-2018 Academic support staff
