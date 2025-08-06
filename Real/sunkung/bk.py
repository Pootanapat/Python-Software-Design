import  firebase_admin
from firebase_admin import credentials, firestore
#เชืิ่อมต่อ Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
    
