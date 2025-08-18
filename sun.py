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
        farm_doc = self.farm_ref.document(farm_id)
        farm = farm_doc.get().to_dict()
        members = farm.get("members", [])
        if member_name in members:
            members.remove(member_name)
            farm_doc.update({"members": members})
            print(f"ลบสมาชิก {member_name} ออกจากฟาร์ม {farm_id}")
            
        def get_farm(self, farm_id):
            """ดึงข้อมูลฟาร์ม"""
            farm = self.farm_ref.get().document(farm_id).to_dict()
            print(f"ข้อมูลฟาร์ม {farm_id}: {farm}")
            return farm
    def list_farms(self):
        """แสดงรายการฟาร์มทั้งหมด"""
        farms = self.farm_ref.stream()
        farm_list = [farm.id for farm in farms]
        print("ฟาร์มทั้งหมด:", farm_list)
        return farm_list
farm = FarmManager()

farm.create_farm("farm01", {"name": "Green farm", "location": "Ladkrabang","members":["sun"]})

#เพิ่มสมาชิก
farm.add_member("farm01", "gun")
# ลบสมาชิก
farm.remove_member("farm01", "sun")
# ดึงข้อมูลฟาร์ม
farm.get_farm("farm01")