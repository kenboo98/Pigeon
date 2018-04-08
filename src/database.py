from pymongo import MongoClient
import sha256

class DB:
    """
        Database setup for MongoDB to be extended by both users
        and posts document class
    """
    def __init__(self):
        # initalizes a connection to database
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.PIGEON

class UserDB(DB):

    """
        Connects to and works with PIGEON MongoDB database to add users and
        login old users

        Status Codes:
            101: Success; New User added successfully
            102: Success; User logged in successfully
            421: U_IDError; User already in database
            431: LoginError; Record not found in database
    """

    def __init__(self):
        super().__init__()

    def create_account(self, u_id, password):
        """
            adds new account to database, password is stored as a sha256 hash
            Args:
                u_id - user email to be added
                password - password to be added (unhashed)
            Returns:
                status code - to signal error or success back to server
        """
        # get users documnet
        users = self.db.users

        # hash user provided password using sha256
        password = sha256.SHA256(password).hexdigest()

        # if user email is already in database
        if (not users.find_one({"u_id": u_id}) is None):
            return 421

        new_user = {"u_id": u_id,
                    "password": password}

        # insert new user to database
        new_user_insert = users.insert_one(new_user)
        return 101

    def verify_login(self, u_id, password):
        """
            verifies user id and password for login
            Args:
                u_id - user email to be added
                password - password to be added (unhashed)
            Returns:
                status code - to signal error or success back to server
        """
        users = self.db.users

        # hash user provided password using sha256
        login_hash = sha256.SHA256(password).hexdigest()

        user = users.find_one({"u_id": u_id})

        # if no user with the u_id is found
        if user is None:
            return 431
        else:
            # compare user hashed password to hash stored in database
            if (user.get('password') == login_hash):
                return 102
            else:
                return 431

class PostsDB(DB):
    """
        Connects to and works with PIGEON MongoDB database to add posts and
        search for posts
    """
    def __init__(self):
        super().__init__()

    def addPost(self, u_id, post, tstamp):
        """
            adds new post to database
            Args:
                u_id - user email which posted new post
                post - the post (message) to be added
                tstamp - time when the post was made
        """
        # get posts document from database
        posts = self.db.posts

        # add new post
        new_post = {"_id": posts.count() + 1,
                    "u_id": u_id,
                    "post": post,
                    "timestamp": tstamp}

        posts.insert_one(new_post)

    def loadLast(self, count, lastLoaded):
        """
            loads last (count) number of messages before the last loaded message
            Args:
                count - number of posts the server wants to load
                lastLoaded - index of last loaded post at top
            Returns:
                last_posts - array of the previous posts loaded
                returnLoadedIndex - New last loaded index
        """
        posts = self.db.posts
        loaded = []
        last_posts = []

        # get last (count) number of posts from db if they exist, else limit the number
        # of posts to be loaded
        load_num = count if lastLoaded - count >= 1 else lastLoaded - 1
        loaded = posts.find({"_id": {"$gte": lastLoaded - load_num, "$lte": lastLoaded - 1}}).sort("_id")

        # clean up posts to be added to a format client expects
        for post in loaded:
            last_posts.append({"author": post.get("u_id"),
                                "message": post.get("post"),
                                "timestamp": post.get("timestamp")})

        # new last loaded index
        returnLoadedIndex = lastLoaded - load_num

        return last_posts, returnLoadedIndex

    def getCount(self):
        """
            returns total number of posts
        """
        return self.db.posts.count()
