import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("test-91b11-firebase-adminsdk-fbsvc-7f08a69953.json")
firebase_admin.initialize_app(cred)
from firebase_admin import firestore

db = firestore.client()

reg = {
    "user": input("Enter username: "),
    "password": input("Enter password: "),
}
user_ref = db.collection("users").document("user1")
user_ref.set(reg)
reg1 = {
    "user": input("Enter username: "),
    "password": input("Enter password: "),
}
user_ref1 = db.collection("users").document("user2")
user_ref1.set(reg1)