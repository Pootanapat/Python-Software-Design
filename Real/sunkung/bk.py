import  firebase_admin
from firebase_admin import credentials, firestore
# Initialize Firebase Admin SDK
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
firebase_admin.initialize_app(cred)             
# Initialize Firestore
db = firestore.client()     
# Function to add a document to a collection
def add_document(collection_name, document_data):           
    collection_ref = db.collection(collection_name)
    collection_ref.add(document_data)
    
