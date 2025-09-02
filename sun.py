import firebase_admin
from firebase_admin import credentials, firestore
import requests


def connect_firebase_with_config():
    """ฟังก์ชันสำหรับเชื่อมต่อ Firebase ด้วย Firebase Config"""
    try:
        # ข้อมูลการกำหนดค่า Firebase (จาก Firebase Console -> Project settings)
        firebase_config = {
            "apiKey": "your_api_key",
            "authDomain": "your_project_id.firebaseapp.com",
            "projectId": "your_project_id",
            "storageBucket": "your_project_id.appspot.com",
            "messagingSenderId": "your_sender_id",
            "appId": "your_app_id"
        }
        
        # สร้าง credential จาก config
        cred = credentials.Certificate({
            "project_id": firebase_config["projectId"],
            "private_key": "ไม่จำเป็นเมื่อใช้ Client SDK",
            "client_email": "ไม่จำเป็นเมื่อใช้ Client SDK",
            "token_uri": "https://oauth2.googleapis.com/token",
        })
        
        # กำหนดค่า OAuth2 สำหรับการยืนยันตัวตน
        from firebase_admin import auth
        import google.auth.transport.requests
        
        # เชื่อมต่อ Firebase
        firebase_admin.initialize_app(cred, {
            'projectId': firebase_config['projectId']
        })
        
        db = firestore.client()
        print("✅ เชื่อมต่อ Firebase ด้วย Firebase Config สำเร็จแล้ว")
        return db

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
        return None

# เรียกใช้งานฟังก์ชันเชื่อมต่อ
if __name__ == "__main__":
    db = connect_firebase_with_config()

    if db:
        # ทดสอบการเชื่อมต่อโดยการอ่าน collection
        print("🔄 กำลังทดสอบการเชื่อมต่อ...")
        try:
            # ลองดึงข้อมูล collections (ไม่ต้องสนใจผล)
            collections = db.collections()
            for collection in collections:
                print(f"พบ Collection: {collection.id}")
            print("✅ การทดสอบการเชื่อมต่อผ่าน")
        except Exception as e:
            print(f"❌ การทดสอบการเชื่อมต่อล้มเหลว: {e}")
    else:
        print("โปรดแก้ไขปัญหาแล้วลองอีกครั้ง")
              
    import requests

class FarmManagerREST:
    def __init__(self, firebase_config):
        self.api_key = firebase_config["apiKey"]
        self.project_id = firebase_config["projectId"]
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{self.project_id}/databases/(default)/documents"

    def create_farm(self, farm_id, data):
        """สร้างฟาร์มใหม่"""
        url = f"{self.base_url}/farms/{farm_id}?key={self.api_key}"
        payload = {"fields": self._convert_data(data)}
        response = requests.patch(url, json=payload)
        print("✅ สร้างฟาร์ม:", response.json())

    def get_farm(self, farm_id):
        """ดึงข้อมูลฟาร์ม"""
        url = f"{self.base_url}/farms/{farm_id}?key={self.api_key}"
        response = requests.get(url)
        print("📌 ข้อมูลฟาร์ม:", response.json())
        return response.json()

    def add_member(self, farm_id, member_name):
        """เพิ่มสมาชิกในฟาร์ม"""
        farm = self.get_farm(farm_id)
        members = [m["stringValue"] for m in farm["fields"].get("members", {}).get("arrayValue", {}).get("values", [])]

        members.append(member_name)
        url = f"{self.base_url}/farms/{farm_id}?key={self.api_key}"
        payload = {"fields": {"members": {"arrayValue": {"values": [{"stringValue": m} for m in members]}}}}
        response = requests.patch(url, json=payload)
        print(f"👤 เพิ่มสมาชิก {member_name}:", response.json())

    def _convert_data(self, data):
        """แปลง dict Python → Firestore REST API format"""
        fields = {}
        for k, v in data.items():
            if isinstance(v, str):
                fields[k] = {"stringValue": v}
            elif isinstance(v, int):
                fields[k] = {"integerValue": str(v)}
            elif isinstance(v, list):
                fields[k] = {"arrayValue": {"values": [{"stringValue": i} for i in v]}}
        return fields


if __name__ == "__main__":
    firebase_config = {
        "apiKey": "YOUR_API_KEY",
        "projectId": "YOUR_PROJECT_ID",
    }

    farm = FarmManagerREST(firebase_config)

    # ✅ สร้างฟาร์มใหม่
    farm.create_farm("farm1", {"name": "Mini Farm", "members": ["Alice"]})

    # 👤 เพิ่มสมาชิก
    farm.add_member("farm1", "Bob")

    # 📌 ดูข้อมูลฟาร์ม
    farm.get_farm("farm1")
