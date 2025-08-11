import  firebase_admin
from firebase_admin import credentials, firestore
#เชืิ่อมต่อ Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class FarmManager:
    def __init__(self):
        self.farm_ref  = db.collection("farms")
    
    def create_farm(self, farm_id, data):
        """สร้างฟาร์มใหม่"""
        self.farm_ref.document(farm_id).set(data)
        print(f"ฟาร์ม {farm_id}ถูกสร้างเเล้ว")
    def add_member(self, farm_id, member_name):
        """เพิ่มสมาชิกในฟาร์ม"""
        farm_doc = self.farm_ref.document(farm_id)
        farm = farm_doc.get().to_dict()
        members =farm.get ("members", [])
        members.append(member_name)
        farm_doc.update({"members": members})
        print(f"เพิ่มสมาชิก{member_name} ในฟาร์ม {farm_id}") 

    def remove_member(self, farm_id, member_name):
        """ลบสมาชิกฟาร์ม"""
