# firebase_service.py
import time
import logging
import pyrebase
form utils import now_ts, sanitize_email

# Setup Logging
logger = logging.getLogger("MINIFARM")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("minifarm.log" , encoding='utf-8')
fh.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
fh.setFormatter(fmt)
logger.addHandler(fh)

# Firebase Configuration
firebaseConfig = {
    "apiKey": "your_api_key",
    "authDomain": "your_project_id.firebaseapp.com",
    "databaseURL": "https://your_project_id.firebaseio.com",
    "projectId": "your_project_id",
    "storageBucket": "your_project_id.appspot.com",
    "messagingSenderId": "your_messaging_sender_id",
    "appId": "your_app_id"
}

#--------------------------------------------------------------------------

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Token expiry margin (seconds) — จะ refresh token ถ้าหมดอายุใน < MARGIN

TOKEN_EXPIRY_MARGIN = 300

class FirebaseServiceError(Exception):
    pass

class FirebaseService:
    def __init__(self):
        self.user = None
        self.token_acquired_at = None

# ----- Auth -----

def signup(self, email: str, password: str):
        try:
            logger.info("Signing up %s", email)
            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']
            profile = {"display_name": email.split("@")[0], "created_at": now_ts()}
            db.child("users").child(uid).set(profile, user['idToken'])
            db.child("users_by_email").child(sanitize_email(email)).set(uid, user['idToken'])
            logger.info("User created %s uid=%s", email, uid)
            return user
        except Exception as e:
            logger.exception("Signup failed")
            raise FirebaseServiceError(str(e))