from pymongo import MongoClient
import datetime
import hashlib

class UserDB:

    """
        Connects to and works with PIGEON MongoDB database to add users and
        login old users

        Error Codes:
            101: Success; New User added successfully
            102: Success; User logged in successfully
            421: U_IDError; User already in database
            431: LoginError; Record not found in database
    """

    def __init__(self):
        # initalizes a connection to database
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.PIGEON

    def create_account(self, u_id, password):
        # get users documnet
        users = self.db.users

        # hash user provided password using sha256
        password = hashlib.sha256(password.encode()).hexdigest()

        # if user email is already in database
        if (not users.find_one({"u_id": u_id}) is None):
            return 421

        new_user = {"u_id": u_id,
                    "password": str(password).upper()}

        # insert new user to database
        new_user_insert = users.insert_one(new_user)
        return 101

    def verify_login(self, u_id, password):
        users = self.db.users

        # hash user provided password using sha256
        password = hashlib.sha256(password.encode()).hexdigest()

        user = users.find_one({"u_id": u_id})

        # if no user with the u_id is found
        if user is None:
            return 431
        else:
            # compare user hashed password to hash stored in database
            db_password_hash = user.get('password')
            login_password_hash = str(password).upper()

            if (db_password_hash == login_password_hash):
                return 102
            else:
                return 431
