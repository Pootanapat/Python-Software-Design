# MINIFARM (Python + Tkinter + Firebase)

แอพจัดการฟาร์มขนาดเล็กที่ใช้ Python (Tkinter) เป็น GUI และเชื่อมต่อกับ Firebase เพื่อจัดเก็บข้อมูลผู้ใช้, ฟาร์ม, สัตว์, พืช และการจัดการสิทธิ์ (Role-based Access)

## ✅ คุณสมบัติ

- **ระบบ Login/Signup** ผ่าน Firebase Authentication
- **สร้างฟาร์มใหม่** หรือ **เข้าร่วมฟาร์มของผู้อื่น** ด้วยอีเมลเจ้าของ
- **ระบบจัดการสิทธิ์ (Role-based permissions)**:
  - `owner`: ดู, เพิ่ม, แก้ไข, ลบ ได้ทั้งหมด
  - `animal_manager`: ดู, เพิ่ม, แก้ไข, ลบ สัตว์
  - `plant_manager`: ดู, เพิ่ม, แก้ไข, ลบ พืช
  - `viewer`: ดูอย่างเดียว
- **ระบบจัดการสัตว์/พืช**:
  - เพิ่ม/แก้ไข/ลบ ข้อมูลสัตว์/พืช
  - บันทึกเวลาล่าสุดที่ให้อาหาร/รดน้ำ (ใช้เวลาของประเทศไทย)
- **ระบบเชิญสมาชิก** และ **ตั้งบทบาท**
- **แสดงกิจกรรม (Log)** (อยู่ในแผนพัฒนา)
- **ปุ่มลบฟาร์ม** (เฉพาะเจ้าของ)

## 📦 โครงสร้างโปรเจกต์

FarmApp_Tkinter/
├── main.py
├── firebase_config.py
├── utils.py
├── requirements.txt
├── screens/
│ ├── login_screen.py
│ ├── signup_screen.py
│ ├── farm_selection_screen.py
│ ├── create_farm_screen.py
│ ├── farm_dashboard.py
│ ├── animal_screen.py
│ ├── plant_screen.py
│ ├── add_animal_screen.py
│ ├── add_plant_screen.py
│ ├── edit_item_screen.py
│ ├── manager_screen.py
│ ├── invite_member_screen.py
│ └── role_permission_screen.py
└── README.md
