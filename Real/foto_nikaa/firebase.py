import firebase_admin
from firebase_admin import credentials, firestore
def initialize_firebase():
    cred = credentials.Certificate('my-small-farm-system-firebase-adminsdk-fbsvc-343c1b46e5.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db