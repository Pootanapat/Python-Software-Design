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
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import uuid

class FarmBackend:
    def __init__(self, credential_path: Optional[str] = None):
        """
        Initialize Firebase connection
        
        Args:
            credential_path: Path to service account key JSON file
        """
        try:
            if not firebase_admin._apps:
                if credential_path:
                    cred = credentials.Certificate(credential_path)
                else:
                    # Try to find service account key in common locations
                    try:
                        cred = credentials.Certificate("serviceAccountKey.json")
                    except:
                        cred = credentials.ApplicationDefault()
                
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            print("✅ Connected to Firebase Firestore successfully")
            
        except Exception as e:
            print(f"❌ Failed to connect to Firebase: {e}")
            raise

    # ===== FARM MANAGEMENT METHODS =====
    
    def create_farm(self, farm_data: Dict, owner_id: str) -> Tuple[bool, str, Optional[str]]:
        """
        สร้างฟาร์มใหม่
        
        Args:
            farm_data: ข้อมูลฟาร์ม {name, description, location, etc.}
            owner_id: ID ของเจ้าของฟาร์ม
            
        Returns:
            (success, message, farm_id)
        """
        try:
            # Generate unique farm ID
            farm_id = f"farm_{uuid.uuid4().hex[:8]}"
            
            # Prepare farm data
            farm_data.update({
                'farm_id': farm_id,
                'owner_id': owner_id,
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP,
                'members': [{
                    'user_id': owner_id,
                    'role': 'owner',
                    'joined_at': firestore.SERVER_TIMESTAMP
                }]
            })
            
            # Save to Firestore
            doc_ref = self.db.collection('farms').document(farm_id)
            doc_ref.set(farm_data)
            
            # Also create a reference in user's farms list
            user_ref = self.db.collection('users').document(owner_id)
            user_ref.update({
                'farms': firestore.ArrayUnion([farm_id])
            })
            
            return True, "สร้างฟาร์มสำเร็จ", farm_id
            
        except Exception as e:
            return False, f"การสร้างฟาร์มล้มเหลว: {e}", None

    def get_farm(self, farm_id: str) -> Optional[Dict]:
        """
        ดึงข้อมูลฟาร์ม
        
        Args:
            farm_id: ID ของฟาร์ม
            
        Returns:
            ข้อมูลฟาร์มหรือ None หากไม่พบ
        """
        try:
            doc_ref = self.db.collection('farms').document(farm_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            print(f"Error getting farm: {e}")
            return None

    def update_farm(self, farm_id: str, update_data: Dict) -> Tuple[bool, str]:
        """
        อัปเดตข้อมูลฟาร์ม
        
        Args:
            farm_id: ID ของฟาร์ม
            update_data: ข้อมูลที่ต้องการอัปเดต
            
        Returns:
            (success, message)
        """
        try:
            # Add updated timestamp
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            doc_ref = self.db.collection('farms').document(farm_id)
            doc_ref.update(update_data)
            
            return True, "อัปเดตข้อมูลฟาร์มสำเร็จ"
            
        except Exception as e:
            return False, f"การอัปเดตข้อมูลฟาร์มล้มเหลว: {e}"

    def delete_farm(self, farm_id: str, user_id: str) -> Tuple[bool, str]:
        """
        ลบฟาร์ม (เฉพาะเจ้าของเท่านั้นที่ลบได้)
        
        Args:
            farm_id: ID ของฟาร์ม
            user_id: ID ของผู้ใช้ที่ต้องการลบ
            
        Returns:
            (success, message)
        """
        try:
            # Check if user is the owner
            farm_data = self.get_farm(farm_id)
            if not farm_data:
                return False, "ไม่พบฟาร์มนี้"
                
            if farm_data.get('owner_id') != user_id:
                return False, "ไม่มีสิทธิ์ลบฟาร์มนี้"
            
            # Delete farm document
            doc_ref = self.db.collection('farms').document(farm_id)
            doc_ref.delete()
            
            # Remove farm reference from all members
            members = farm_data.get('members', [])
            for member in members:
                user_ref = self.db.collection('users').document(member['user_id'])
                user_ref.update({
                    'farms': firestore.ArrayRemove([farm_id])
                })
            
            return True, "ลบฟาร์มสำเร็จ"
            
        except Exception as e:
            return False, f"การลบฟาร์มล้มเหลว: {e}"

    def get_user_farms(self, user_id: str) -> List[Dict]:
        """
        ดึงฟาร์มทั้งหมดที่ผู้ใช้เป็นสมาชิกหรือเจ้าของ
        
        Args:
            user_id: ID ของผู้ใช้
            
        Returns:
            รายการฟาร์ม
        """
        try:
            # Query farms where user is a member
            farms_ref = self.db.collection('farms')
            query = farms_ref.where('members', 'array_contains', {'user_id': user_id})
            
            results = query.stream()
            user_farms = []
            
            for doc in results:
                farm_data = doc.to_dict()
                farm_data['id'] = doc.id
                user_farms.append(farm_data)
            
            return user_farms
            
        except Exception as e:
            print(f"Error getting user farms: {e}")
            return []

    # ===== MEMBER MANAGEMENT METHODS =====
    
    def add_member(self, farm_id: str, user_id: str, role: str = 'member', 
                  added_by: str = None) -> Tuple[bool, str]:
        """
        เพิ่มสมาชิกเข้าไปในฟาร์ม
        
        Args:
            farm_id: ID ของฟาร์ม
            user_id: ID ของผู้ใช้ที่จะเพิ่ม
            role: บทบาท (owner, manager, member, viewer)
            added_by: ID ของผู้ที่เพิ่มสมาชิก
            
        Returns:
            (success, message)
        """
        try:
            # Check if user exists
            user_ref = self.db.collection('users').document(user_id)
            if not user_ref.get().exists:
                return False, "ไม่พบผู้ใช้นี้ในระบบ"
            
            # Check if user is already a member
            farm_data = self.get_farm(farm_id)
            if not farm_data:
                return False, "ไม่พบฟาร์มนี้"
                
            current_members = farm_data.get('members', [])
            for member in current_members:
                if member['user_id'] == user_id:
                    return False, "ผู้ใช้นี้เป็นสมาชิกอยู่แล้ว"
            
            # Add new member
            new_member = {
                'user_id': user_id,
                'role': role,
                'joined_at': firestore.SERVER_TIMESTAMP,
                'added_by': added_by
            }
            
            # Update farm members
            doc_ref = self.db.collection('farms').document(farm_id)
            doc_ref.update({
                'members': firestore.ArrayUnion([new_member]),
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            # Add farm to user's farm list
            user_ref.update({
                'farms': firestore.ArrayUnion([farm_id])
            })
            
            return True, "เพิ่มสมาชิกสำเร็จ"
            
        except Exception as e:
            return False, f"การเพิ่มสมาชิกล้มเหลว: {e}"

    def remove_member(self, farm_id: str, user_id: str, removed_by: str) -> Tuple[bool, str]:
        """
        ลบสมาชิกออกจากฟาร์ม
        
        Args:
            farm_id: ID ของฟาร์ม
            user_id: ID ของผู้ใช้ที่จะลบ
            removed_by: ID ของผู้ที่ลบสมาชิก
            
        Returns:
            (success, message)
        """
        try:
            farm_data = self.get_farm(farm_id)
            if not farm_data:
                return False, "ไม่พบฟาร์มนี้"
            
            # Check permissions (only owner can remove members)
            if farm_data.get('owner_id') != removed_by:
                return False, "ไม่มีสิทธิ์ลบสมาชิก"
                
            # Cannot remove owner
            if user_id == farm_data.get('owner_id'):
                return False, "ไม่สามารถลบเจ้าของฟาร์มได้"
            
            # Find and remove the member
            current_members = farm_data.get('members', [])
            member_to_remove = None
            
            for member in current_members:
                if member['user_id'] == user_id:
                    member_to_remove = member
                    break
            
            if not member_to_remove:
                return False, "ไม่พบสมาชิกนี้ในฟาร์ม"
            
            # Remove member from farm
            doc_ref = self.db.collection('farms').document(farm_id)
            doc_ref.update({
                'members': firestore.ArrayRemove([member_to_remove]),
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            # Remove farm from user's farm list
            user_ref = self.db.collection('users').document(user_id)
            user_ref.update({
                'farms': firestore.ArrayRemove([farm_id])
            })
            
            return True, "ลบสมาชิกสำเร็จ"
            
        except Exception as e:
            return False, f"การลบสมาชิกล้มเหลว: {e}"

    def update_member_role(self, farm_id: str, user_id: str, new_role: str, 
                          updated_by: str) -> Tuple[bool, str]:
        """
        อัปเดตบทบาทของสมาชิก
        
        Args:
            farm_id: ID ของฟาร์ม
            user_id: ID ของผู้ใช้
            new_role: บทบาทใหม่
            updated_by: ID ของผู้ที่อัปเดต
            
        Returns:
            (success, message)
        """
        try:
            farm_data = self.get_farm(farm_id)
            if not farm_data:
                return False, "ไม่พบฟาร์มนี้"
            
            # Check permissions (only owner can update roles)
            if farm_data.get('owner_id') != updated_by:
                return False, "ไม่มีสิทธิ์อัปเดตบทบาท"
            
            # Get current members
            current_members = farm_data.get('members', [])
            updated_members = []
            member_found = False
            
            for member in current_members:
                if member['user_id'] == user_id:
                    # Update the role
                    member['role'] = new_role
                    member_found = True
                updated_members.append(member)
            
            if not member_found:
                return False, "ไม่พบสมาชิกนี้ในฟาร์ม"
            
            # Update the members list
            doc_ref = self.db.collection('farms').document(farm_id)
            doc_ref.update({
                'members': updated_members,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            return True, "อัปเดตบทบาทสำเร็จ"
            
        except Exception as e:
            return False, f"การอัปเดตบทบาทล้มเหลว: {e}"

    def get_farm_members(self, farm_id: str) -> List[Dict]:
        """
        ดึงรายการสมาชิกทั้งหมดของฟาร์ม
        
        Args:
            farm_id: ID ของฟาร์ม
            
        Returns:
            รายการสมาชิก
        """
        try:
            farm_data = self.get_farm(farm_id)
            if not farm_data:
                return []
            
            members = farm_data.get('members', [])
            
            # Enrich member data with user information
            enriched_members = []
            for member in members:
                user_data = self.get_user_info(member['user_id'])
                if user_data:
                    member_data = member.copy()
                    member_data.update(user_data)
                    enriched_members.append(member_data)
            
            return enriched_members
            
        except Exception as e:
            print(f"Error getting farm members: {e}")
            return []

    # ===== USER MANAGEMENT METHODS =====
    
    def create_user(self, user_data: Dict) -> Tuple[bool, str]:
        """
        สร้างผู้ใช้ใหม่
        
        Args:
            user_data: ข้อมูลผู้ใช้ {username, email, display_name, etc.}
            
        Returns:
            (success, message)
        """
        try:
            user_id = user_data.get('user_id') or f"user_{uuid.uuid4().hex[:8]}"
            
            # Check if user already exists
            user_ref = self.db.collection('users').document(user_id)
            if user_ref.get().exists:
                return False, "มีผู้ใช้นี้อยู่แล้ว"
            
            # Prepare user data
            user_data.update({
                'user_id': user_id,
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP,
                'farms': []  # Initialize empty farms list
            })
            
            # Save to Firestore
            user_ref.set(user_data)
            
            return True, "สร้างผู้ใช้สำเร็จ"
            
        except Exception as e:
            return False, f"การสร้างผู้ใช้ล้มเหลว: {e}"

    def get_user_info(self, user_id: str) -> Optional[Dict]:
        """
        ดึงข้อมูลผู้ใช้
        
        Args:
            user_id: ID ของผู้ใช้
            
        Returns:
            ข้อมูลผู้ใช้หรือ None หากไม่พบ
        """
        try:
            user_ref = self.db.collection('users').document(user_id)
            doc = user_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None

    # ===== UTILITY METHODS =====
    
    def check_farm_permission(self, farm_id: str, user_id: str, 
                             required_role: str = None) -> Tuple[bool, str]:
        """
        ตรวจสอบสิทธิ์การเข้าถึงฟาร์ม
        
        Args:
            farm_id: ID ของฟาร์ม
            user_id: ID ของผู้ใช้
            required_role: บทบาทที่ต้องการ (ถ้าไม่指定ให้ตรวจสอบแค่ความเป็นสมาชิก)
            
        Returns:
            (has_permission, message)
        """
        try:
            farm_data = self.get_farm(farm_id)
            if not farm_data:
                return False, "ไม่พบฟาร์มนี้"
            
            # Check if user is a member
            members = farm_data.get('members', [])
            user_role = None
            
            for member in members:
                if member['user_id'] == user_id:
                    user_role = member['role']
                    break
            
            if not user_role:
                return False, "ไม่ใช่สมาชิกของฟาร์มนี้"
            
            # If specific role is required, check it
            if required_role:
                role_hierarchy = {'owner': 3, 'manager': 2, 'member': 1, 'viewer': 0}
                user_level = role_hierarchy.get(user_role, -1)
                required_level = role_hierarchy.get(required_role, -1)
                
                if user_level < required_level:
                    return False, f"ต้องการบทบาท {required_role} หรือสูงกว่า"
            
            return True, "มีสิทธิ์เข้าถึง"
            
        except Exception as e:
            return False, f"การตรวจสอบสิทธิ์ล้มเหลว: {e}"

# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    # Initialize backend
    backend = FarmBackend("serviceAccountKey.json")  # หรือไม่ระบุ path ถ้าใช้ default credentials
    
    # สร้างผู้ใช้ตัวอย่าง
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'display_name': 'Test User'
    }
    success, message = backend.create_user(user_data)
    print(f"Create user: {success} - {message}")
    
    # สร้างฟาร์มตัวอย่าง
    farm_data = {
        'name': 'ฟาร์มตัวอย่าง',
        'description': 'ฟาร์มสำหรับทดสอบระบบ',
        'location': 'เชียงใหม่'
    }
    success, message, farm_id = backend.create_farm(farm_data, 'user_testuser')
    print(f"Create farm: {success} - {message} - Farm ID: {farm_id}")
    
    # ดึงข้อมูลฟาร์ม
    farm_info = backend.get_farm(farm_id)
    print(f"Farm info: {farm_info}")
    
    # ดึงฟาร์มของผู้ใช้
    user_farms = backend.get_user_farms('user_testuser')
    print(f"User farms: {len(user_farms)} farms")
    
    # ตรวจสอบสิทธิ์
    has_permission, perm_message = backend.check_farm_permission(farm_id, 'user_testuser', 'owner')
    print(f"Permission check: {has_permission} - {perm_message}")

    # Initialize
backend = FarmBackend("path/to/serviceAccountKey.json")

# สร้างฟาร์ม
farm_data = {
    'name': 'ชื่อฟาร์มของคุณ',
    'description': 'คำอธิบายฟาร์ม',
    'location': 'ที่ตั้งฟาร์ม'
}
success, message, farm_id = backend.create_farm(farm_data, 'user_id_of_owner')

# จัดการสมาชิก
backend.add_member(farm_id, 'user_id_to_add', 'member', 'user_id_who_adds')

# ดึงข้อมูล
farms = backend.get_user_farms('user_id')
members = backend.get_farm_members(farm_id)