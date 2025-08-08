
# 🌿 Project Minifarm - ระบบจัดการฟาร์มอัจฉริยะ (Smart Farm Management System)

## 📌 คำอธิบายโปรเจกต์ | Project Description
Minifarm เป็นแอปพลิเคชันบนระบบปฏิบัติการ Windows ที่พัฒนาโดยใช้ภาษา Python และ Tkinter สำหรับจัดการฟาร์มในรูปแบบจำลอง โดยเชื่อมต่อกับ Firebase Admin SDK เพื่อให้สามารถสมัครสมาชิก เข้าสู่ระบบ และเลือกฟาร์มได้

Minifarm is a Windows desktop application developed using Python and Tkinter. It allows users to register, log in, and manage farms by connecting to Firebase Admin SDK. The application simulates a smart farm dashboard with basic functionality.

---

## 🛠 เทคโนโลยีที่ใช้ | Technologies Used
- Python 3
- Tkinter (for GUI)
- Firebase Admin SDK (for authentication and future data handling)
- Firebase Service Account Key (.json)

---

## 📦 การติดตั้งและใช้งาน | Installation & Usage

1. **ติดตั้งไลบรารีที่จำเป็น | Install required libraries**:
```bash
pip install firebase-admin
```

2. **ดาวน์โหลดไฟล์ Service Account Key (.json)** จาก Firebase Console:
- ไปที่ `Project Settings > Service Accounts`
- คลิก "Generate new private key"
- วางไฟล์ไว้ในโฟลเดอร์เดียวกับ `main.py`
- แก้ไขชื่อไฟล์ในตัวแปร `SERVICE_ACCOUNT_KEY_PATH` ให้ตรงกับชื่อไฟล์ของคุณ

Download the Service Account Key file from your Firebase project and place it in the same directory as `main.py`. Update the `SERVICE_ACCOUNT_KEY_PATH` variable if needed.

3. **รันแอปพลิเคชัน | Run the application**:
```bash
python main.py
```

---

## ✨ ฟีเจอร์หลัก | Main Features
- ✅ ระบบสมัครสมาชิก (User Registration)
- ✅ ระบบเข้าสู่ระบบ (User Login)
- ✅ หน้าจอเลือกฟาร์ม (Farm Selection)
- ✅ แดชบอร์ดฟาร์มจำลอง (Dashboard overview with fake data)
- ⏳ การจัดการฟาร์ม: พืช สัตว์ กิจกรรม สมาชิก (อยู่ระหว่างการพัฒนา)
  (Plant, Animal, Activity, and Member management are under development)

---

## ⚠️ หมายเหตุ | Notes
- การตรวจสอบรหัสผ่านใน Firebase Admin SDK โดยตรงไม่สามารถทำได้จริง
  (No real password verification is available through Firebase Admin SDK)
- ในโปรเจกต์จริงควรใช้ Firebase Client SDK หรือ Firebase REST API สำหรับการยืนยันตัวตนอย่างปลอดภัย
  (For production use, Firebase Client SDK or REST API should be used for secure login)

---

## 👨‍💻 ผู้พัฒนา | Developer
- [Pootanapat Takimnok]
- Email: 68030231@kmitl.ac.th
- Email: 68030049@kmitl.ac.th

หากพบปัญหาหรือข้อเสนอแนะ สามารถติดต่อผู้พัฒนาได้ทางอีเมลด้านบน

If you have issues or suggestions, feel free to contact the developer.
