# File: /login-system-app/login-system-app/src/users.py

users = {
    "admin": "1234",
    "user": "abcd"
}

def add_user(username, password):
    if username not in users:
        users[username] = password
        return True
    return False

def remove_user(username):
    if username in users:
        del users[username]
        return True
    return False

def get_users():
    return users.keys()