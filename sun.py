import firebase_admin
from firebase_admin import credentials, firestore
import json

def connect_firebase():
    """ฟังก์ชันสำหรับเชื่อมต่อ Firebase โดยสร้างไฟล์ service account ชั่วคราว"""
    try:
        # ข้อมูล service account
        service_account_info = {
            "type": "service_account",
            "project_id": "my-small-farm-system",
            "private_key_id": "your_actual_private_key_id",
            "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_ACTUAL_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-xxxxx@my-small-farm-system.iam.gserviceaccount.com",
            "client_id": "your_actual_client_id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40my-small-farm-system.iam.gserviceaccount.com"
        }
        
        # สร้างไฟล์ service account ชั่วคราว
        with open('temp_service_account.json', 'w') as f:
            json.dump(service_account_info, f)
        
        # ตรวจสอบว่าแอป Firebase ถูก initialize แล้วหรือยัง
        if not firebase_admin._apps:
            cred = credentials.Certificate('temp_service_account.json')
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("✅ เชื่อมต่อ Firebase สำเร็จแล้ว")
        
        # ลบไฟล์ชั่วคราว (optional)
        import os
        os.remove('temp_service_account.json')
        
        return db

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
        return None

import firebase_admin
from firebase_admin import credentials, firestore
from typing import List, Dict, Optional
import os
import json

def connect_firebase():
    """ฟังก์ชันสำหรับเชื่อมต่อ Firebase โดยไม่ต้องใช้ไฟล์ JSON แยก"""
    try:
        # ตรวจสอบว่าแอป Firebase ถูก initialize แล้วหรือยัง
        if not firebase_admin._apps:
            # ใช้ environment variables สำหรับการกำหนดค่า
            # หากไม่มี environment variables ให้ใช้ค่าจากโค้ดโดยตรง
            firebase_config = {
                "type": os.environ.get("FIREBASE_TYPE", "service_account"),
                "project_id": os.environ.get("FIREBASE_PROJECT_ID", "my-small-farm-system"),
                "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID", "your_private_key_id_here"),
                "private_key": os.environ.get("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n'),
                "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL", "firebase-adminsdk@my-small-farm-system.iam.gserviceaccount.com"),
                "client_id": os.environ.get("FIREBASE_CLIENT_ID", "your_client_id_here"),
                "auth_uri": os.environ.get("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
                "token_uri": os.environ.get("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
                "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
                "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL", "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk%40my-small-farm-system.iam.gserviceaccount.com")
            }
            
            # ตรวจสอบว่ามี private key หรือไม่
            if not firebase_config["private_key"]:
                print("⚠️  ไม่พบ private key, กำลังลองใช้ Firebase Emulator...")
                try:
                    # ลองใช้ Firebase Emulator (สำหรับการพัฒนา)
                    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
                    cred = credentials.ApplicationDefault()
                    firebase_admin.initialize_app(cred, {
                        'projectId': firebase_config['project_id']
                    })
                except Exception as emulator_error:
                    print(f"❌ ไม่สามารถเชื่อมต่อกับ Emulator: {emulator_error}")
                    return None
            else:
                # ใช้ credentials จาก config
                cred = credentials.Certificate(firebase_config)
                firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("✅ เชื่อมต่อ Firebase สำเร็จแล้ว")
        return db

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
        print("⚠️  กำลังสวิตช์ไปใช้โหมดจำลอง (Simulation Mode)...")
        return None

class FarmManager:
    def __init__(self, db):
        self.db = db
        self.current_farm_id = None
        self.simulation_mode = db is None
        
        if self.simulation_mode:
            print("🔶 ทำงานในโหมดจำลอง (Simulation Mode)")
            # สร้างข้อมูลจำลองสำหรับทดสอบ
            self.mock_farms = {
                "farm001": {
                    "name": "ฟาร์มสวนผลไม้อุเล (จำลอง)",
                    "owner": "user001",
                    "description": "ฟาร์มผลไม้ organic แบบพอเพียง - ข้อมูลจำลอง",
                    "location": "เชียงใหม่",
                    "members": [
                        {"id": "user001", "name": "สมชาย", "role": "owner"},
                        {"id": "user002", "name": "สมหญิง", "role": "manager"}
                    ],
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00"
                }
            }

    def create_farm(self, farm_id: str, data: Dict):
        """สร้างฟาร์มใหม่"""
        if self.simulation_mode:
            # โหมดจำลอง
            if farm_id in self.mock_farms:
                print("❌ มีฟาร์มนี้อยู่แล้วในระบบ (จำลอง)")
                return False
            
            self.mock_farms[farm_id] = data
            self.mock_farms[farm_id]['created_at'] = "2023-01-01T00:00:00"
            self.mock_farms[farm_id]['updated_at'] = "2023-01-01T00:00:00"
            print("✅ สร้างฟาร์มสำเร็จ (จำลอง)")
            return True
        
        try:
            # ตรวจสอบว่ามีฟาร์มนี้อยู่แล้วหรือไม่
            if self.db.collection('farms').document(farm_id).get().exists:
                print("❌ มีฟาร์มนี้อยู่แล้วในระบบ")
                return False
            
            doc_ref = self.db.collection('farms').document(farm_id)
            # เพิ่มฟิลด์ created_at และ updated_at
            data['created_at'] = firestore.SERVER_TIMESTAMP
            data['updated_at'] = firestore.SERVER_TIMESTAMP
            doc_ref.set(data)
            print("✅ สร้างฟาร์มสำเร็จ")
            return True
        except Exception as e:
            print(f"❌ การสร้างฟาร์มล้มเหลว: {e}")
            return False

    def get_farm(self, farm_id: str) -> Optional[Dict]:
        """ดึงข้อมูลฟาร์ม"""
        if self.simulation_mode:
            # โหมดจำลอง
            if farm_id in self.mock_farms:
                farm_data = self.mock_farms[farm_id]
                print("📌 ข้อมูลฟาร์ม (จำลอง):", farm_data)
                return farm_data
            else:
                print("❌ ไม่พบฟาร์มนี้ (จำลอง)")
                return None
        
        try:
            doc_ref = self.db.collection('farms').document(farm_id)
            doc = doc_ref.get()
            if doc.exists:
                farm_data = doc.to_dict()
                print("📌 ข้อมูลฟาร์ม:", farm_data)
                return farm_data
            else:
                print("❌ ไม่พบฟาร์มนี้")
                return None
        except Exception as e:
            print(f"❌ ไม่สามารถดึงข้อมูลฟาร์มได้: {e}")
            return None

    def update_farm(self, farm_id: str, update_data: Dict):
        """อัปเดตข้อมูลฟาร์ม"""
        if self.simulation_mode:
            # โหมดจำลอง
            if farm_id not in self.mock_farms:
                print("❌ ไม่พบฟาร์มนี้ (จำลอง)")
                return False
            
            self.mock_farms[farm_id].update(update_data)
            self.mock_farms[farm_id]['updated_at'] = "2023-01-01T00:00:00"
            print("✅ อัปเดตข้อมูลฟาร์มสำเร็จ (จำลอง)")
            return True
        
        try:
            doc_ref = self.db.collection('farms').document(farm_id)
            # เพิ่มฟิลด์ updated_at
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP
            doc_ref.update(update_data)
            print("✅ อัปเดตข้อมูลฟาร์มสำเร็จ")
            return True
        except Exception as e:
            print(f"❌ การอัปเดตข้อมูลฟาร์มล้มเหลว: {e}")
            return False

    def delete_farm(self, farm_id: str):
        """ลบฟาร์ม"""
        if self.simulation_mode:
            # โหมดจำลอง
            if farm_id not in self.mock_farms:
                print("❌ ไม่พบฟาร์มนี้ (จำลอง)")
                return False
            
            del self.mock_farms[farm_id]
            print("✅ ลบฟาร์มสำเร็จ (จำลอง)")
            return True
        
        try:
            # ตรวจสอบสิทธิ์ก่อนลบ (ในที่นี้ให้ตรวจสอบจาก owner)
            doc_ref = self.db.collection('farms').document(farm_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                print("❌ ไม่พบฟาร์มนี้")
                return False
                
            # ในระบบจริงควรตรวจสอบว่า user ปัจจุบันเป็นเจ้าของฟาร์มหรือไม่
            doc_ref.delete()
            print("✅ ลบฟาร์มสำเร็จ")
            return True
        except Exception as e:
            print(f"❌ การลบฟาร์มล้มเหลว: {e}")
            return False

    def add_member(self, farm_id: str, member_data: Dict):
        """เพิ่มสมาชิกในฟาร์ม"""
        if self.simulation_mode:
            # โหมดจำลอง
            if farm_id not in self.mock_farms:
                print("❌ ไม่พบฟาร์มนี้ (จำลอง)")
                return False
            
            if 'members' not in self.mock_farms[farm_id]:
                self.mock_farms[farm_id]['members'] = []
            
            self.mock_farms[farm_id]['members'].append(member_data)
            print(f"✅ เพิ่มสมาชิก {member_data.get('name', 'ไม่มีชื่อ')} สำเร็จ (จำลอง)")
            return True
        
        try:
            doc_ref = self.db.collection('farms').document(farm_id)
            
            # ตรวจสอบว่าฟาร์มมีอยู่จริง
            if not doc_ref.get().exists:
                print("❌ ไม่พบฟาร์มนี้")
                return False
            
            # อัปเดตข้อมูลโดยเพิ่มสมาชิกใหม่เข้าไปในอาร์เรย์
            doc_ref.update({
                'members': firestore.ArrayUnion([member_data]),
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            print(f"✅ เพิ่มสมาชิก {member_data.get('name', 'ไม่มีชื่อ')} สำเร็จ")
            return True
        except Exception as e:
            print(f"❌ การเพิ่มสมาชิกล้มเหลว: {e}")
            return False

    def remove_member(self, farm_id: str, member_id: str):
        """ลบสมาชิกออกจากฟาร์ม"""
        if self.simulation_mode:
            # โหมดจำลอง
            if farm_id not in self.mock_farms:
                print("❌ ไม่พบฟาร์มนี้ (จำลอง)")
                return False
                
            if 'members' not in self.mock_farms[farm_id]:
                print("❌ ไม่มีสมาชิกในฟาร์มนี้ (จำลอง)")
                return False
            
            # ค้นหาและลบสมาชิกตาม member_id
            self.mock_farms[farm_id]['members'] = [
                m for m in self.mock_farms[farm_id]['members'] if m.get('id') != member_id
            ]
            
            print(f"✅ ลบสมาชิก ID {member_id} ออกสำเร็จ (จำลอง)")
            return True
        
        try:
            doc_ref = self.db.collection('farms').document(farm_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                print("❌ ไม่พบฟาร์มนี้")
                return False
                
            farm_data = doc.to_dict()
            members = farm_data.get('members', [])
            
            # ค้นหาและลบสมาชิกตาม member_id
            updated_members = [m for m in members if m.get('id') != member_id]
            
            # อัปเดตข้อมูลฟาร์ม
            doc_ref.update({
                'members': updated_members,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            print(f"✅ ลบสมาชิก ID {member_id} ออกสำเร็จ")
            return True
        except Exception as e:
            print(f"❌ การลบสมาชิกล้มเหลว: {e}")
            return False

    def get_user_farms(self, user_id: str) -> List[Dict]:
        """ดึงฟาร์มทั้งหมดที่ user เป็นสมาชิกหรือเจ้าของ"""
        if self.simulation_mode:
            # โหมดจำลอง
            user_farms = []
            for farm_id, farm_data in self.mock_farms.items():
                # ตรวจสอบว่า user เป็นเจ้าของหรือสมาชิก
                if farm_data.get('owner') == user_id:
                    farm_data_copy = farm_data.copy()
                    farm_data_copy['id'] = farm_id
                    user_farms.append(farm_data_copy)
                else:
                    # ตรวจสอบในสมาชิก
                    for member in farm_data.get('members', []):
                        if member.get('id') == user_id:
                            farm_data_copy = farm_data.copy()
                            farm_data_copy['id'] = farm_id
                            user_farms.append(farm_data_copy)
                            break
            
            print(f"✅ พบฟาร์มทั้งหมด {len(user_farms)} ฟาร์ม (จำลอง)")
            return user_farms
        
        try:
            # ค้นหาฟาร์มทั้งหมดที่ user นี้เป็นสมาชิก
            farms_ref = self.db.collection('farms')
            query = farms_ref.where('members', 'array_contains', {'id': user_id})
            
            results = query.stream()
            user_farms = []
            
            for doc in results:
                farm_data = doc.to_dict()
                farm_data['id'] = doc.id
                user_farms.append(farm_data)
            
            print(f"✅ พบฟาร์มทั้งหมด {len(user_farms)} ฟาร์ม")
            return user_farms
        except Exception as e:
            print(f"❌ ไม่สามารถดึงฟาร์มของผู้ใช้ได้: {e}")
            return []

    def set_current_farm(self, farm_id: str):
        """ตั้งค่าฟาร์มปัจจุบันที่กำลังทำงาน"""
        if self.simulation_mode:
            # โหมดจำลอง
            if farm_id in self.mock_farms:
                self.current_farm_id = farm_id
                print(f"✅ ตั้งค่าฟาร์มปัจจุบันเป็น: {farm_id} (จำลอง)")
                return True
            else:
                print("❌ ไม่พบฟาร์มนี้ (จำลอง)")
                return False
        
        try:
            # ตรวจสอบว่าฟาร์มมีอยู่จริง
            doc_ref = self.db.collection('farms').document(farm_id)
            if doc_ref.get().exists:
                self.current_farm_id = farm_id
                print(f"✅ ตั้งค่าฟาร์มปัจจุบันเป็น: {farm_id}")
                return True
            else:
                print("❌ ไม่พบฟาร์มนี้")
                return False
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการตั้งค่าฟาร์ม: {e}")
            return False

    def get_current_farm(self) -> Optional[Dict]:
        """ดึงข้อมูลฟาร์มปัจจุบัน"""
        if not self.current_farm_id:
            print("❌ ยังไม่ได้เลือกฟาร์ม")
            return None
        
        return self.get_farm(self.current_farm_id)

    def list_all_farms(self) -> List[Dict]:
        """ดึงข้อมูลฟาร์มทั้งหมด (สำหรับผู้ดูแลระบบ)"""
        if self.simulation_mode:
            # โหมดจำลอง
            all_farms = []
            for farm_id, farm_data in self.mock_farms.items():
                farm_data_copy = farm_data.copy()
                farm_data_copy['id'] = farm_id
                all_farms.append(farm_data_copy)
            
            print(f"✅ พบฟาร์มทั้งหมด {len(all_farms)} ฟาร์ม (จำลอง)")
            return all_farms
        
        try:
            farms_ref = self.db.collection('farms')
            docs = farms_ref.stream()
            
            all_farms = []
            for doc in docs:
                farm_data = doc.to_dict()
                farm_data['id'] = doc.id
                all_farms.append(farm_data)
            
            print(f"✅ พบฟาร์มทั้งหมด {len(all_farms)} ฟาร์ม")
            return all_farms
        except Exception as e:
            print(f"❌ ไม่สามารถดึงข้อมูลฟาร์มทั้งหมดได้: {e}")
            return []


# ฟังก์ชันสำหรับทดสอบระบบ
def test_farm_system():
    """ทดสอบการทำงานของระบบจัดการฟาร์ม"""
    db = connect_firebase()
    
    # สร้าง FarmManager (จะทำงานในโหมดจำลองหากไม่สามารถเชื่อมต่อ Firebase ได้)
    farm_manager = FarmManager(db)
    
    # ทดสอบสร้างฟาร์มใหม่
    farm_data = {
        "name": "ฟาร์มสวนผลไม้อุเล",
        "owner": "user001",
        "description": "ฟาร์มผลไม้ organic แบบพอเพียง",
        "location": "เชียงใหม่",
        "members": [
            {"id": "user001", "name": "สมชาย", "role": "owner"},
            {"id": "user002", "name": "สมหญิง", "role": "manager"}
        ]
    }
    
    # สร้างฟาร์ม
    if farm_manager.create_farm("farm001", farm_data):
        print("✅ ทดสอบสร้างฟาร์มสำเร็จ")
    
    # ดึงข้อมูลฟาร์ม
    farm_info = farm_manager.get_farm("farm001")
    if farm_info:
        print("✅ ทดสอบดึงข้อมูลฟาร์มสำเร็จ")
    
    # เพิ่มสมาชิกใหม่
    new_member = {"id": "user003", "name": "สมนึก", "role": "worker"}
    if farm_manager.add_member("farm001", new_member):
        print("✅ ทดสอบเพิ่มสมาชิกสำเร็จ")
    
    # ตั้งค่าฟาร์มปัจจุบัน
    if farm_manager.set_current_farm("farm001"):
        print("✅ ทดสอบตั้งค่าฟาร์มปัจจุบันสำเร็จ")
    
    # ดึงฟาร์มปัจจุบัน
    current_farm = farm_manager.get_current_farm()
    if current_farm:
        print("✅ ทดสอบดึงฟาร์มปัจจุบันสำเร็จ")
    
    # ดึงฟาร์มทั้งหมดของ user
    user_farms = farm_manager.get_user_farms("user001")
    if user_farms:
        print(f"✅ ทดสอบดึงฟาร์มของผู้ใช้สำเร็จ: {len(user_farms)} ฟาร์ม")
    
    # ลบสมาชิก
    if farm_manager.remove_member("farm001", "user003"):
        print("✅ ทดสอบลบสมาชิกสำเร็จ")
    
    # อัปเดตข้อมูลฟาร์ม
    update_data = {"description": "ฟาร์มผลไม้ organic แบบพอเพียง ปรับปรุงใหม่"}
    if farm_manager.update_farm("farm001", update_data):
        print("✅ ทดสอบอัปเดตฟาร์มสำเร็จ")
    
    # แสดงฟาร์มทั้งหมด
    all_farms = farm_manager.list_all_farms()
    print(f"✅ ทดสอบแสดงฟาร์มทั้งหมดสำเร็จ: {len(all_farms)} ฟาร์ม")
    
    # ลบฟาร์ม (ควรปิดการใช้งานในระบบจริง)
    if farm_manager.delete_farm("farm001"):
        print("✅ ทดสอบลบฟาร์มสำเร็จ")

def demo_farm_management():
    """สาธิตการใช้งานระบบจัดการฟาร์ม"""
    db = connect_firebase()
    farm_manager = FarmManager(db)
    
    print("\n" + "="*50)
    print("สาธิตการใช้งานระบบจัดการฟาร์มอุเล")
    print("="*50)
    
    # 1. สร้างฟาร์มตัวอย่าง
    print("\n1. การสร้างฟาร์มใหม่")
    farm_data = {
        "name": "สวนส้มอุเล",
        "owner": "user123",
        "description": "สวนส้ม organic คุณภาพสูง",
        "location": "เชียงใหม่",
        "members": [
            {"id": "user123", "name": "นายอุเล", "role": "owner"},
            {"id": "user456", "name": "นางสาวสมศรี", "role": "manager"}
        ]
    }
    
    farm_manager.create_farm("farm_demo", farm_data)
    
    # 2. แสดงข้อมูลฟาร์ม
    print("\n2. แสดงข้อมูลฟาร์ม")
    farm_info = farm_manager.get_farm("farm_demo")
    if farm_info:
        print(f"ชื่อฟาร์ม: {farm_info.get('name')}")
        print(f"คำอธิบาย: {farm_info.get('description')}")
        print(f"ที่ตั้ง: {farm_info.get('location')}")
        print(f"จำนวนสมาชิก: {len(farm_info.get('members', []))}")
    
    # 3. เพิ่มสมาชิกใหม่
    print("\n3. เพิ่มสมาชิกใหม่")
    new_member = {"id": "user789", "name": "นายสมหมาย", "role": "worker"}
    farm_manager.add_member("farm_demo", new_member)
    
    # 4. ตั้งค่าฟาร์มปัจจุบัน
    print("\n4. ตั้งค่าฟาร์มปัจจุบัน")
    farm_manager.set_current_farm("farm_demo")
    current_farm = farm_manager.get_current_farm()
    if current_farm:
        print(f"ฟาร์มปัจจุบัน: {current_farm.get('name')}")
    
    # 5. แสดงฟาร์มทั้งหมดของผู้ใช้
    print("\n5. แสดงฟาร์มทั้งหมดของผู้ใช้")
    user_farms = farm_manager.get_user_farms("user123")
    for i, farm in enumerate(user_farms, 1):
        print(f"{i}. {farm.get('name')} - {farm.get('location')}")
    
    print("\n✅ สาธิตการใช้งานเสร็จสิ้น")

if __name__ == "__main__":
    # รันการทดสอบระบบ
    test_farm_system()
    
    # รันการสาธิต
    demo_farm_management()