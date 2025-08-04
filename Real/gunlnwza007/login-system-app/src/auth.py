# File: /login-system-app/login-system-app/src/auth.py

users = {
    "admin": "1234",
    "user": "abcd"
}

def login(username, password):
    if username in users and users[username] == password:
        return True
    return False

def register(username, password):
    if username not in users:
        users[username] = password
        return True
    return False

def change_password(username, old_password, new_password):
    if username in users and users[username] == old_password:
        users[username] = new_password
        return True
    return False