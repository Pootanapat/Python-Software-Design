import firebase_admin
from firebase_admin import credentials, firestore
def initialize_firebase():
    cred = credentials.Certificate('my-small-farm-system-firebase-adminsdk-fbsvc-343c1b46e5.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

SERVICE_ACCOUNT_KEY_PATH = "my-small-farm-system-firebase-adminsdk-fbsvc-343c1b46e5.json"

# --- Initialize Firebase Admin SDK ---
try:
    # Debug prints to check the file path
    current_directory = os.getcwd()
    full_key_path = os.path.join(current_directory, SERVICE_ACCOUNT_KEY_PATH)
    print(f"Current working directory: {current_directory}")
    print(f"Attempting to load service account key from: {full_key_path}")

    # ตรวจสอบว่าไฟล์มีอยู่จริงหรือไม่
    if not os.path.exists(full_key_path):
        raise FileNotFoundError(f"Service account key file not found at: {full_key_path}")

    # ตรวจสอบว่า Firebase Admin SDK ยังไม่ได้ถูก Initialise
    if not firebase_admin._apps:
        cred = credentials.Certificate(full_key_path) # ใช้ full_key_path เพื่อความแน่นอน
        firebase_admin.initialize_app(cred)
    
    # สำหรับ firebase-admin, auth object จะถูกเข้าถึงโดยตรงจาก firebase_admin.auth
    # ไม่ใช่จาก pyrebase
    print(f"Firebase Admin SDK initialized successfully.")
except FileNotFoundError as e:
    messagebox.showerror("Firebase Initialization Error", f"Failed to initialize Firebase Admin SDK: {e}\nPlease ensure your service account key path is correct and the file exists.")
    exit()
except Exception as e:
    messagebox.showerror("Firebase Initialization Error", f"Failed to initialize Firebase Admin SDK: {e}\nPlease ensure your service account key path is correct and the file exists.")
    exit() # ออกจากโปรแกรมหาก Firebase Initialise ไม่สำเร็จ
import os
from tkinter import messagebox
# --- Initialize Firebase Firestore ---
db = initialize_firebase()
# --- Firebase Firestore Database Reference ---
def get_firestore_db():
    return db
# --- Firebase Firestore Database Reference ---
def get_firestore_collection(collection_name):
    return db.collection(collection_name)
# --- Firebase Firestore Document Reference ---
def get_firestore_document(collection_name, document_id):
    return db.collection(collection_name).document(document_id)
# --- Firebase Firestore Query ---
def get_firestore_query(collection_name, query):
    return db.collection(collection_name).where(**query)
# --- Firebase Firestore Add Document ---
def add_firestore_document(collection_name, data):
    return db.collection(collection_name).add(data)
# --- Firebase Firestore Update Document ---
def update_firestore_document(collection_name, document_id, data):
    return db.collection(collection_name).document(document_id).update(data)
# --- Firebase Firestore Delete Document ---
def delete_firestore_document(collection_name, document_id):
    return db.collection(collection_name).document(document_id).delete()
# --- Firebase Firestore Get Document ---
def get_firestore_document(collection_name, document_id):
    return db.collection(collection_name).document(document_id).get().to_dict()
def get_firestore_all_documents(collection_name):
    return {doc.id: doc.to_dict() for doc in db.collection(collection_name).get().documents}
