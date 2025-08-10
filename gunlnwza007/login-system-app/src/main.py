# File: /login-system-app/login-system-app/src/main.py

from auth import login
from users import users

def main():
    username = input("Username: ")
    password = input("Password: ")

    if login(username, password):
        print("Login successful!")
    else:
        print("Login failed. Please check your credentials and try again.")

if __name__ == "__main__":
    main()