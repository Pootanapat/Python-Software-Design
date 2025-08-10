users = {
    "admin": "1234",
    "user": "abcd"
}

def check_login(username, password):
    """
    ตรวจสอบชื่อผู้ใช้และรหัสผ่าน
    คืนค่า True ถ้าข้อมูลถูกต้อง, False ถ้าไม่ถูกต้อง
    """
    return username in users and users[username] == password