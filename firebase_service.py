# firebase_service.py
import time
import logging
import pyrebase
from utils import now_ts, sanitize_email

# ----------------- Setup logging -----------------
logger = logging.getLogger("MINIFARM")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("minifarm.log", encoding="utf-8")
fh.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
fh.setFormatter(fmt)
logger.addHandler(fh)

# ----------------- Firebase config (แก้ให้เป็นของคุณ) -----------------
firebaseConfig = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
    "databaseURL": "https://YOUR_PROJECT_ID.firebaseio.com",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_PROJECT_ID.appspot.com",
    "messagingSenderId": "YOUR_SENDER_ID",
    "appId": "YOUR_APP_ID"
}
# ---------------------------------------------------------------------

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Token expiry margin (seconds) — จะ refresh token ถ้าหมดอายุใน < MARGIN
TOKEN_EXPIRY_MARGIN = 300  # 5 minutes

class FirebaseServiceError(Exception):
    pass

class FirebaseService:
    def __init__(self):
        self.user = None  # dict from pyrebase auth (idToken, refreshToken, localId, expiresIn)
        self.token_acquired_at = None

    # ---------- Auth ----------
    def signup(self, email: str, password: str):
        try:
            logger.info("Signing up %s", email)
            user = auth.create_user_with_email_and_password(email, password)
            # create user profile record and mapping by email for lookup
            uid = user['localId']
            profile = {"display_name": email.split("@")[0], "created_at": now_ts()}
            db.child("users").child(uid).set(profile, user['idToken'])
            db.child("users_by_email").child(sanitize_email(email)).set(uid, user['idToken'])
            logger.info("User created %s uid=%s", email, uid)
            return user
        except Exception as e:
            logger.exception("Signup failed")
            raise FirebaseServiceError(str(e))

    def login(self, email: str, password: str):
        try:
            logger.info("Login attempt %s", email)
            user = auth.sign_in_with_email_and_password(email, password)
            self.user = user
            self.token_acquired_at = time.time()
            # store expiresIn (string seconds) if available
            logger.info("Login success uid=%s", user.get("localId"))
            return user
        except Exception as e:
            logger.exception("Login failed")
            raise FirebaseServiceError(str(e))

    def _need_refresh(self):
        if not self.user or 'expiresIn' not in self.user:
            return False
        try:
            expires = int(self.user.get("expiresIn", 3600))
        except:
            expires = 3600
        if not self.token_acquired_at:
            return True
        remain = (self.token_acquired_at + expires) - time.time()
        return remain < TOKEN_EXPIRY_MARGIN

    def ensure_token(self):
        if not self.user:
            raise FirebaseServiceError("Not logged in")
        if self._need_refresh():
            try:
                logger.info("Refreshing token for uid=%s", self.user.get('localId'))
                refreshed = auth.refresh(self.user['refreshToken'])
                # refreshed: idToken, userId, refreshToken, expiresIn
                self.user.update(refreshed)
                self.token_acquired_at = time.time()
                logger.info("Token refreshed")
            except Exception as e:
                logger.exception("Token refresh failed")
                raise FirebaseServiceError("Token refresh failed: " + str(e))

    def logout(self):
        logger.info("User logout uid=%s", self.user.get("localId") if self.user else None)
        self.user = None
        self.token_acquired_at = None

    # ---------- Basic DB wrappers ----------
    def db_get(self, path: str):
        try:
            self.ensure_token()
            token = self.user['idToken']
            return db.child(path).get(token)
        except Exception as e:
            logger.exception("db_get failed: %s", path)
            # try refreshing once
            try:
                self.ensure_token()
                token = self.user['idToken']
                return db.child(path).get(token)
            except Exception as e2:
                logger.exception("db_get retry failed")
                raise FirebaseServiceError(str(e2))

    def db_set(self, path: str, value):
        try:
            self.ensure_token()
            token = self.user['idToken']
            return db.child(path).set(value, token)
        except Exception as e:
            logger.exception("db_set failed: %s", path)
            raise FirebaseServiceError(str(e))

    def db_push(self, path: str, value):
        try:
            self.ensure_token()
            token = self.user['idToken']
            return db.child(path).push(value, token)
        except Exception as e:
            logger.exception("db_push failed: %s", path)
            raise FirebaseServiceError(str(e))

    def db_update(self, path: str, value):
        try:
            self.ensure_token()
            token = self.user['idToken']
            return db.child(path).update(value, token)
        except Exception as e:
            logger.exception("db_update failed: %s", path)
            raise FirebaseServiceError(str(e))

    def db_remove(self, path: str):
        try:
            self.ensure_token()
            token = self.user['idToken']
            return db.child(path).remove(token)
        except Exception as e:
            logger.exception("db_remove failed: %s", path)
            raise FirebaseServiceError(str(e))

    # ---------- App-specific helpers ----------
    def create_farm(self, name: str):
        """
        Create a farm in /farms/{farm_id} and set member role for owner;
        also create reference in user_farms/{uid}/{farm_id}=role
        """