import hashlib

def initialize():
    global pw_file
    global pw_dict
    pw_dict = {}
    pw_file = open("passwords", "w+")
    line = pw_file.readline().strip()
    while(line):
        pw_dict[line] = pw_file.readline().strip()
        line = pw_file.readline().strip()


def create_account(username, password):
    hasher = hashlib.sha256()
    pw_file.write(username + "\n")
    hasher.update(password.encode())
    pw_file.write(str(hasher.hexdigest()) + "\n")
    pw_dict[username] = str(hasher.hexdigest())

def verify_login(username, password):
    try:
        hasher = hashlib.sha256()
        hasher.update(password.encode())
        return str(hasher.hexdigest()) == pw_dict[username]
    except KeyError:
        return "KeyError"
