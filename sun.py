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

import sys
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Optional, Tuple

# สำหรับ Firebase (จะใช้โหมดจำลองหากไม่สามารถเชื่อมต่อได้)
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("⚠️  Firebase not available, using simulation mode")

class FarmManager:
    def __init__(self):
        self.db = None
        self.current_farm_id = None
        self.simulation_mode = True
        self.mock_farms = {}
        
        if FIREBASE_AVAILABLE:
            self.db = self.connect_firebase()
            if self.db:
                self.simulation_mode = False
                print("✅ Connected to Firebase")
            else:
                print("🔶 Using simulation mode")
        
        # สร้างข้อมูลจำลองเริ่มต้น
        self.init_mock_data()
    
    def connect_firebase(self):
        """เชื่อมต่อ Firebase"""
        try:
            if not firebase_admin._apps:
                # ลองหาไฟล์ service account
                if os.path.exists("serviceAccountKey.json"):
                    cred = credentials.Certificate("serviceAccountKey.json")
                    firebase_admin.initialize_app(cred)
                    return firestore.client()
                else:
                    print("⚠️  serviceAccountKey.json not found")
                    return None
            return firestore.client()
        except Exception as e:
            print(f"❌ Firebase connection error: {e}")
            return None
    
    def init_mock_data(self):
        """เตรียมข้อมูลจำลองสำหรับทดสอบ"""
        self.mock_farms = {
            "farm001": {
                "name": "สวนส้มอุเล",
                "owner": "user001",
                "description": "สวนส้ม organic คุณภาพสูง",
                "location": "เชียงใหม่",
                "members": [
                    {"id": "user001", "name": "นายอุเล", "role": "owner", "email": "ule@example.com"},
                    {"id": "user002", "name": "นางสาวสมศรี", "role": "manager", "email": "somsri@example.com"}
                ],
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            },
            "farm002": {
                "name": "ฟาร์มไก่ไข่อุเล",
                "owner": "user001",
                "description": "ฟาร์มไก่ไข่อินทรีย์",
                "location": "ลำพูน",
                "members": [
                    {"id": "user001", "name": "นายอุเล", "role": "owner", "email": "ule@example.com"},
                    {"id": "user003", "name": "นายสมชาย", "role": "caretaker", "email": "somchai@example.com"}
                ],
                "created_at": "2023-02-15T00:00:00",
                "updated_at": "2023-02-15T00:00:00"
            }
        }
    
    def create_farm(self, farm_id: str, data: Dict) -> Tuple[bool, str]:
        """สร้างฟาร์มใหม่"""
        if self.simulation_mode:
            if farm_id in self.mock_farms:
                return False, "มีฟาร์มนี้อยู่แล้วในระบบ"
            
            self.mock_farms[farm_id] = data
            self.mock_farms[farm_id]['created_at'] = "2023-01-01T00:00:00"
            self.mock_farms[farm_id]['updated_at'] = "2023-01-01T00:00:00"
            return True, "สร้างฟาร์มสำเร็จ"
        
        try:
            if self.db.collection('farms').document(farm_id).get().exists:
                return False, "มีฟาร์มนี้อยู่แล้วในระบบ"
            
            doc_ref = self.db.collection('farms').document(farm_id)
            data['created_at'] = firestore.SERVER_TIMESTAMP
            data['updated_at'] = firestore.SERVER_TIMESTAMP
            doc_ref.set(data)
            return True, "สร้างฟาร์มสำเร็จ"
        except Exception as e:
            return False, f"การสร้างฟาร์มล้มเหลว: {e}"
    
    def get_farm(self, farm_id: str) -> Optional[Dict]:
        """ดึงข้อมูลฟาร์ม"""
        if self.simulation_mode:
            return self.mock_farms.get(farm_id)
        
        try:
            doc_ref = self.db.collection('farms').document(farm_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"ไม่สามารถดึงข้อมูลฟาร์มได้: {e}")
            return None
    
    def get_all_farms(self) -> Dict:
        """ดึงฟาร์มทั้งหมด"""
        if self.simulation_mode:
            return self.mock_farms
        
        try:
            farms_ref = self.db.collection('farms')
            docs = farms_ref.stream()
            
            all_farms = {}
            for doc in docs:
                farm_data = doc.to_dict()
                farm_data['id'] = doc.id
                all_farms[doc.id] = farm_data
            
            return all_farms
        except Exception as e:
            print(f"ไม่สามารถดึงข้อมูลฟาร์มทั้งหมดได้: {e}")
            return {}
    
    def update_farm(self, farm_id: str, update_data: Dict) -> Tuple[bool, str]:
        """อัปเดตข้อมูลฟาร์ม"""
        if self.simulation_mode:
            if farm_id not in self.mock_farms:
                return False, "ไม่พบฟาร์มนี้"
            
            self.mock_farms[farm_id].update(update_data)
            self.mock_farms[farm_id]['updated_at'] = "2023-01-01T00:00:00"
            return True, "อัปเดตข้อมูลฟาร์มสำเร็จ"
        
        try:
            doc_ref = self.db.collection('farms').document(farm_id)
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP
            doc_ref.update(update_data)
            return True, "อัปเดตข้อมูลฟาร์มสำเร็จ"
        except Exception as e:
            return False, f"การอัปเดตข้อมูลฟาร์มล้มเหลва: {e}"
    
    def delete_farm(self, farm_id: str) -> Tuple[bool, str]:
        """ลบฟาร์ม"""
        if self.simulation_mode:
            if farm_id not in self.mock_farms:
                return False, "ไม่พบฟาร์มนี้"
            
            del self.mock_farms[farm_id]
            return True, "ลบฟาร์มสำเร็จ"
        
        try:
            doc_ref = self.db.collection('farms').document(farm_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return False, "ไม่พบฟาร์มนี้"
                
            doc_ref.delete()
            return True, "ลบฟาร์มสำเร็จ"
        except Exception as e:
            return False, f"การลบฟาร์มล้มเหลว: {e}"
    
    def add_member(self, farm_id: str, member_data: Dict) -> Tuple[bool, str]:
        """เพิ่มสมาชิกในฟาร์ม"""
        if self.simulation_mode:
            if farm_id not in self.mock_farms:
                return False, "ไม่พบฟาร์มนี้"
            
            if 'members' not in self.mock_farms[farm_id]:
                self.mock_farms[farm_id]['members'] = []
            
            # ตรวจสอบว่าสมาชิกมีอยู่แล้วหรือไม่
            for member in self.mock_farms[farm_id]['members']:
                if member.get('id') == member_data.get('id'):
                    return False, "มีสมาชิกนี้อยู่แล้วในฟาร์ม"
            
            self.mock_farms[farm_id]['members'].append(member_data)
            return True, f"เพิ่มสมาชิก {member_data.get('name', '')} สำเร็จ"
        
        try:
            doc_ref = self.db.collection('farms').document(farm_id)
            
            if not doc_ref.get().exists:
                return False, "ไม่พบฟาร์มนี้"
            
            doc_ref.update({
                'members': firestore.ArrayUnion([member_data]),
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            return True, f"เพิ่มสมาชิก {member_data.get('name', '')} สำเร็จ"
        except Exception as e:
            return False, f"การเพิ่มสมาชิกล้มเหลว: {e}"
    
    def remove_member(self, farm_id: str, member_id: str) -> Tuple[bool, str]:
        """ลบสมาชิกออกจากฟาร์ม"""
        if self.simulation_mode:
            if farm_id not in self.mock_farms:
                return False, "ไม่พบฟาร์มนี้"
                
            if 'members' not in self.mock_farms[farm_id]:
                return False, "ไม่มีสมาชิกในฟาร์มนี้"
            
            # ค้นหาและลบสมาชิกตาม member_id
            original_count = len(self.mock_farms[farm_id]['members'])
            self.mock_farms[farm_id]['members'] = [
                m for m in self.mock_farms[farm_id]['members'] if m.get('id') != member_id
            ]
            
            if len(self.mock_farms[farm_id]['members']) == original_count:
                return False, "ไม่พบสมาชิกนี้ในฟาร์ม"
            
            return True, "ลบสมาชิกออกสำเร็จ"
        
        try:
            doc_ref = self.db.collection('farms').document(farm_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return False, "ไม่พบฟาร์มนี้"
                
            farm_data = doc.to_dict()
            members = farm_data.get('members', [])
            
            # ค้นหาและลบสมาชิกตาม member_id
            updated_members = [m for m in members if m.get('id') != member_id]
            
            if len(updated_members) == len(members):
                return False, "ไม่พบสมาชิกนี้ในฟาร์ม"
            
            doc_ref.update({
                'members': updated_members,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            return True, "ลบสมาชิกออกสำเร็จ"
        except Exception as e:
            return False, f"การลบสมาชิกล้มเหลว: {e}"

class LoginWindow:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.window = tk.Tk()
        self.window.title("ระบบจัดการมินิฟาร์ม - เข้าสู่ระบบ")
        self.window.geometry("400x300")
        self.window.configure(padx=20, pady=20)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.window, text="ระบบจัดการมินิฟาร์ม", 
                              font=("Bai Jamjuree", 18, "bold"))
        title_label.pack(pady=10)
        
        # Logo placeholder
        logo_label = tk.Label(self.window, text="🐓", font=("Arial", 48))
        logo_label.pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(self.window)
        form_frame.pack(pady=20, fill="x")
        
        # Username
        tk.Label(form_frame, text="ชื่อผู้ใช้:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(form_frame, width=35)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Password
        tk.Label(form_frame, text="รหัสผ่าน:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(form_frame, width=35, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Buttons frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)
        
        # Login button
        login_btn = tk.Button(button_frame, text="เข้าสู่ระบบ", 
                             command=self.login, width=15, height=2)
        login_btn.pack(pady=5)
        
        # Demo login button
        demo_btn = tk.Button(button_frame, text="เข้าสู่ระบบแบบทดสอบ", 
                            command=self.demo_login, width=15, height=2)
        demo_btn.pack(pady=5)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน")
            return
        
        # ในระบบจริงควรตรวจสอบกับฐานข้อมูล
        if username == "admin" and password == "password":
            self.window.destroy()
            self.parent_app.show_main_app()
        else:
            messagebox.showwarning("แจ้งเตือน", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    
    def demo_login(self):
        self.window.destroy()
        self.parent_app.show_main_app()
    
    def run(self):
        self.window.mainloop()

class FarmForm:
    def __init__(self, parent, farm_manager):
        self.parent = parent
        self.farm_manager = farm_manager
        self.current_farm_id = None
        
        self.frame = ttk.Frame(parent)
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.frame, text="ข้อมูลฟาร์ม", 
                              font=("Bai Jamjuree", 14, "bold"))
        title_label.pack(pady=10)
        
        # Form
        form_frame = ttk.Frame(self.frame)
        form_frame.pack(pady=10, fill="x", padx=20)
        
        # Farm ID
        ttk.Label(form_frame, text="รหัสฟาร์ม:").grid(row=0, column=0, sticky="w", pady=5)
        self.farm_id_entry = ttk.Entry(form_frame, width=30)
        self.farm_id_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Farm Name
        ttk.Label(form_frame, text="ชื่อฟาร์ม:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Location
        ttk.Label(form_frame, text="ที่ตั้ง:").grid(row=2, column=0, sticky="w", pady=5)
        self.location_entry = ttk.Entry(form_frame, width=30)
        self.location_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Description
        ttk.Label(form_frame, text="คำอธิบาย:").grid(row=3, column=0, sticky="nw", pady=5)
        self.desc_text = scrolledtext.ScrolledText(form_frame, width=25, height=5)
        self.desc_text.grid(row=3, column=1, pady=5, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=10)
        
        self.save_btn = ttk.Button(button_frame, text="บันทึก", command=self.save_farm)
        self.save_btn.pack(side="left", padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="ล้างข้อมูล", command=self.clear_form)
        self.clear_btn.pack(side="left", padx=5)
        
        self.delete_btn = ttk.Button(button_frame, text="ลบฟาร์ม", command=self.delete_farm)
        self.delete_btn.pack(side="left", padx=5)
        self.delete_btn.state(["disabled"])
    
    def clear_form(self):
        self.farm_id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.desc_text.delete(1.0, tk.END)
        self.current_farm_id = None
        self.delete_btn.state(["disabled"])
        self.farm_id_entry.config(state="normal")
    
    def load_farm(self, farm_id):
        farm_data = self.farm_manager.get_farm(farm_id)
        if farm_data:
            self.current_farm_id = farm_id
            self.farm_id_entry.delete(0, tk.END)
            self.farm_id_entry.insert(0, farm_id)
            self.farm_id_entry.config(state="disabled")
            
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, farm_data.get('name', ''))
            
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, farm_data.get('location', ''))
            
            self.desc_text.delete(1.0, tk.END)
            self.desc_text.insert(1.0, farm_data.get('description', ''))
            
            self.delete_btn.state(["!disabled"])
    
    def save_farm(self):
        farm_id = self.farm_id_entry.get()
        name = self.name_entry.get()
        location = self.location_entry.get()
        description = self.desc_text.get(1.0, tk.END).strip()
        
        if not farm_id or not name:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกรหัสฟาร์มและชื่อฟาร์ม")
            return
        
        farm_data = {
            'name': name,
            'location': location,
            'description': description,
            'owner': 'user001'  # ในระบบจริงควรใช้ ID ผู้ใช้ที่ล็อกอิน
        }
        
        if self.current_farm_id:
            # อัปเดตฟาร์มที่มีอยู่
            success, message = self.farm_manager.update_farm(self.current_farm_id, farm_data)
        else:
            # สร้างฟาร์มใหม่
            success, message = self.farm_manager.create_farm(farm_id, farm_data)
        
        if success:
            messagebox.showinfo("สำเร็จ", message)
            self.clear_form()
            # รีเฟรชรายการฟาร์ม
            if hasattr(self.parent, 'refresh_farm_list'):
                self.parent.refresh_farm_list()
        else:
            messagebox.showerror("ข้อผิดพลาด", message)
    
    def delete_farm(self):
        if not self.current_farm_id:
            return
        
        result = messagebox.askyesno("ยืนยันการลบ", 
                                    f"คุณแน่ใจว่าต้องการลบฟาร์ม {self.current_farm_id} นี้ใช่หรือไม่?")
        
        if result:
            success, message = self.farm_manager.delete_farm(self.current_farm_id)
            if success:
                messagebox.showinfo("สำเร็จ", message)
                self.clear_form()
                # รีเฟรชรายการฟาร์ม
                if hasattr(self.parent, 'refresh_farm_list'):
                    self.parent.refresh_farm_list()
            else:
                messagebox.showerror("ข้อผิดพลาด", message)

class MemberForm:
    def __init__(self, parent, farm_manager):
        self.parent = parent
        self.farm_manager = farm_manager
        self.current_farm_id = None
        
        self.frame = ttk.Frame(parent)
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.frame, text="จัดการสมาชิกฟาร์ม", 
                              font=("Bai Jamjuree", 14, "bold"))
        title_label.pack(pady=10)
        
        # Farm selection
        farm_frame = ttk.Frame(self.frame)
        farm_frame.pack(pady=5, fill="x", padx=20)
        
        ttk.Label(farm_frame, text="เลือกฟาร์ม:").pack(side="left")
        self.farm_combo = ttk.Combobox(farm_frame, state="readonly", width=27)
        self.farm_combo.pack(side="left", padx=5)
        self.farm_combo.bind("<<ComboboxSelected>>", self.farm_selected)
        
        # Member form
        form_frame = ttk.Frame(self.frame)
        form_frame.pack(pady=10, fill="x", padx=20)
        
        ttk.Label(form_frame, text="รหัสสมาชิก:").grid(row=0, column=0, sticky="w", pady=5)
        self.member_id_entry = ttk.Entry(form_frame, width=30)
        self.member_id_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="ชื่อสมาชิก:").grid(row=1, column=0, sticky="w", pady=5)
        self.member_name_entry = ttk.Entry(form_frame, width=30)
        self.member_name_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="อีเมล:").grid(row=2, column=0, sticky="w", pady=5)
        self.member_email_entry = ttk.Entry(form_frame, width=30)
        self.member_email_entry.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="บทบาท:").grid(row=3, column=0, sticky="w", pady=5)
        self.member_role_combo = ttk.Combobox(form_frame, values=["owner", "manager", "worker", "viewer"], width=27)
        self.member_role_combo.grid(row=3, column=1, pady=5, padx=5)
        self.member_role_combo.current(0)
        
        # Add member button
        self.add_btn = ttk.Button(self.frame, text="เพิ่มสมาชิก", command=self.add_member)
        self.add_btn.pack(pady=5)
        self.add_btn.state(["disabled"])
        
        # Members table title
        table_title = tk.Label(self.frame, text="สมาชิกในฟาร์ม", font=("Bai Jamjuree", 12))
        table_title.pack(pady=10)
        
        # Members table
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(pady=5, fill="both", expand=True, padx=20)
        
        # Create treeview (table)
        columns = ("id", "name", "email", "role")
        self.members_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        
        # Define headings
        self.members_table.heading("id", text="รหัส")
        self.members_table.heading("name", text="ชื่อ")
        self.members_table.heading("email", text="อีเมล")
        self.members_table.heading("role", text="บทบาท")
        
        # Set column widths
        self.members_table.column("id", width=80)
        self.members_table.column("name", width=120)
        self.members_table.column("email", width=150)
        self.members_table.column("role", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.members_table.yview)
        self.members_table.configure(yscrollcommand=scrollbar.set)
        
        self.members_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Remove button
        self.remove_btn = ttk.Button(self.frame, text="ลบสมาชิกที่เลือก", command=self.remove_member)
        self.remove_btn.pack(pady=5)
        self.remove_btn.state(["disabled"])
        
        # Bind selection event
        self.members_table.bind("<<TreeviewSelect>>", self.on_table_select)
    
    def refresh_farm_list(self):
        farms = self.farm_manager.get_all_farms()
        self.farm_combo['values'] = list(farms.keys())
    
    def farm_selected(self, event):
        self.current_farm_id = self.farm_combo.get()
        self.add_btn.state(["!disabled"])
        self.update_members_table()
    
    def update_members_table(self):
        # Clear table
        for item in self.members_table.get_children():
            self.members_table.delete(item)
        
        if not self.current_farm_id:
            return
        
        farm_data = self.farm_manager.get_farm(self.current_farm_id)
        if not farm_data or 'members' not in farm_data:
            return
        
        # Add members to table
        for member in farm_data['members']:
            self.members_table.insert("", "end", values=(
                member.get('id', ''),
                member.get('name', ''),
                member.get('email', ''),
                member.get('role', '')
            ))
    
    def on_table_select(self, event):
        selected = self.members_table.selection()
        if selected:
            self.remove_btn.state(["!disabled"])
        else:
            self.remove_btn.state(["disabled"])
    
    def add_member(self):
        if not self.current_farm_id:
            return
        
        member_id = self.member_id_entry.get()
        member_name = self.member_name_entry.get()
        member_email = self.member_email_entry.get()
        member_role = self.member_role_combo.get()
        
        if not member_id or not member_name:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกรหัสและชื่อสมาชิก")
            return
        
        member_data = {
            'id': member_id,
            'name': member_name,
            'email': member_email,
            'role': member_role
        }
        
        success, message = self.farm_manager.add_member(self.current_farm_id, member_data)
        if success:
            messagebox.showinfo("สำเร็จ", message)
            self.member_id_entry.delete(0, tk.END)
            self.member_name_entry.delete(0, tk.END)
            self.member_email_entry.delete(0, tk.END)
            self.update_members_table()
        else:
            messagebox.showerror("ข้อผิดพลาด", message)
    
    def remove_member(self):
        if not self.current_farm_id:
            return
        
        selected = self.members_table.selection()
        if not selected:
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกสมาชิกที่ต้องการลบ")
            return
        
        member_id = self.members_table.item(selected[0])['values'][0]
        
        result = messagebox.askyesno("ยืนยันการลบ", 
                                    f"คุณแน่ใจว่าต้องการลบสมาชิก {member_id} นี้ใช่หรือไม่?")
        
        if result:
            success, message = self.farm_manager.remove_member(self.current_farm_id, member_id)
            if success:
                messagebox.showinfo("สำเร็จ", message)
                self.update_members_table()
                self.remove_btn.state(["disabled"])
            else:
                messagebox.showerror("ข้อผิดพลาด", message)

class FarmList:
    def __init__(self, parent, farm_manager):
        self.parent = parent
        self.farm_manager = farm_manager
        
        self.frame = ttk.Frame(parent)
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.frame, text="รายการฟาร์มทั้งหมด", 
                              font=("Bai Jamjuree", 14, "bold"))
        title_label.pack(pady=10)
        
        # Table frame
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        # Create treeview (table)
        columns = ("id", "name", "location", "members")
        self.farms_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Define headings
        self.farms_table.heading("id", text="รหัสฟาร์ม")
        self.farms_table.heading("name", text="ชื่อฟาร์ม")
        self.farms_table.heading("location", text="ที่ตั้ง")
        self.farms_table.heading("members", text="จำนวนสมาชิก")
        
        # Set column widths
        self.farms_table.column("id", width=100)
        self.farms_table.column("name", width=150)
        self.farms_table.column("location", width=120)
        self.farms_table.column("members", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.farms_table.yview)
        self.farms_table.configure(yscrollcommand=scrollbar.set)
        
        self.farms_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double click event
        self.farms_table.bind("<Double-1>", self.on_double_click)
        
        # Refresh button
        refresh_btn = ttk.Button(self.frame, text="รีเฟรชข้อมูล", command=self.refresh_farm_list)
        refresh_btn.pack(pady=10)
        
        self.refresh_farm_list()
    
    def refresh_farm_list(self):
        # Clear table
        for item in self.farms_table.get_children():
            self.farms_table.delete(item)
        
        farms = self.farm_manager.get_all_farms()
        
        # Add farms to table
        for farm_id, farm_data in farms.items():
            member_count = len(farm_data.get('members', []))
            self.farms_table.insert("", "end", values=(
                farm_id,
                farm_data.get('name', ''),
                farm_data.get('location', ''),
                member_count
            ))
    
    def on_double_click(self, event):
        selected = self.farms_table.selection()
        if selected:
            farm_id = self.farms_table.item(selected[0])['values'][0]
            if hasattr(self.parent, 'load_farm'):
                self.parent.load_farm(farm_id)
                self.parent.select_tab(0)  # Switch to farm form tab

class MainApp:
    def __init__(self):
        self.farm_manager = FarmManager()
        self.window = tk.Tk()
        self.window.title("ระบบจัดการมินิฟาร์ม")
        self.window.geometry("800x600")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Create notebook (tab control)
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create farm form tab
        self.farm_form = FarmForm(self, self.farm_manager)
        self.notebook.add(self.farm_form.frame, text="จัดการฟาร์ม")
        
        # Create member form tab
        self.member_form = MemberForm(self, self.farm_manager)
        self.notebook.add(self.member_form.frame, text="จัดการสมาชิก")
        
        # Create farm list tab
        self.farm_list = FarmList(self, self.farm_manager)
        self.notebook.add(self.farm_list.frame, text="รายการฟาร์ม")
        
        # Status bar
        self.status_var = tk.StringVar()
        if self.farm_manager.simulation_mode:
            self.status_var.set("โหมดจำลอง - กำลังทำงานด้วยข้อมูลทดสอบ")
        else:
            self.status_var.set("เชื่อมต่อกับ Firebase แล้ว")
        
        status_bar = ttk.Label(self.window, textvariable=self.status_var, relief="sunken")
        status_bar.pack(side="bottom", fill="x")
    
    def refresh_farm_list(self):
        """รีเฟรชรายการฟาร์มในทุกแท็บที่เกี่ยวข้อง"""
        self.farm_list.refresh_farm_list()
        self.member_form.refresh_farm_list()
        """โหลดข้อมูลฟาร์มเข้าฟอร์มจัดการ"""
        self.farm_form.load_farm(farm_id)
    
    def select_tab(self, tab_index):
        """เลือกแท็บตาม index ที่กำหนด"""
        self.notebook.select(tab_index)
    
    def show(self):
        """แสดงหน้าต่างหลัก"""
        self.window.mainloop()

class FarmManagementApp:
    def __init__(self):
        self.login_window = None
        self.main_app = None
    
    def show_login(self):
        """แสดงหน้าต่างล็อกอิน"""
        self.login_window = LoginWindow(self)
        self.login_window.run()
    
    def show_main_app(self):
        """แสดงแอปหลัก"""
        if self.main_app is None:
            self.main_app = MainApp()
        self.main_app.show()

# เรียกใช้งานแอปพลิเคชัน
if __name__ == "__main__":
    app = FarmManagementApp()
    app.show_login()  
def connect_firebase():
    """เชื่อมต่อ Firebase"""
    