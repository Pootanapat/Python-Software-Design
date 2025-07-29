import firebase_admin
from firebase_admin import credentials, firestore

# โหลดไฟล์ service account จาก Firebase Console
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# เชื่อมต่อ Firestore
db = firestore.client()
