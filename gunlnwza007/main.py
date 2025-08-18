import tkinter as tk  # นำเข้าโมดูล tkinter สำหรับสร้าง GUI
from tkinter import messagebox  # นำเข้า messagebox สำหรับแสดงกล่องข้อความ

users = {
    "admin": "1234",  # กำหนด username และ password เริ่มต้น
    "user": "abcd"
}

def open_register(root):  # ฟังก์ชันเปิดหน้าต่างสมัครสมาชิก
    reg_win = tk.Toplevel(root)  # สร้างหน้าต่างใหม่
    reg_win.title("สมัครสมาชิก")  # ตั้งชื่อหน้าต่าง
    reg_win.geometry("300x180")  # กำหนดขนาดหน้าต่าง

    tk.Label(reg_win, text="Username:").grid(row=0, column=0, pady=5, sticky="e")  # ป้ายชื่อ Username
    reg_username = tk.Entry(reg_win)  # ช่องกรอก Username
    reg_username.grid(row=0, column=1, pady=5)

    tk.Label(reg_win, text="Password:").grid(row=1, column=0, pady=5, sticky="e")  # ป้ายชื่อ Password
    reg_password = tk.Entry(reg_win, show="*")  # ช่องกรอก Password (ซ่อนตัวอักษร)
    reg_password.grid(row=1, column=1, pady=5)

    def register():  # ฟังก์ชันย่อยสำหรับสมัครสมาชิก
        username = reg_username.get()  # รับค่าจากช่องกรอก Username
        password = reg_password.get()  # รับค่าจากช่องกรอก Password
        if username in users:  # ตรวจสอบว่า Username ซ้ำหรือไม่
            messagebox.showerror("ผิดพลาด", "Username นี้มีอยู่แล้ว")
        elif not username or not password:  # ตรวจสอบว่ากรอกข้อมูลครบหรือไม่
            messagebox.showerror("ผิดพลาด", "กรุณากรอกข้อมูลให้ครบ")
        else:
            users[username] = password  # เพิ่มข้อมูลผู้ใช้ใหม่
            messagebox.showinfo("สำเร็จ", "สมัครสมาชิกสำเร็จ!")
            reg_win.destroy()  # ปิดหน้าต่างสมัครสมาชิก

    tk.Button(reg_win, text="สมัครสมาชิก", command=register, width=15).grid(row=2, column=0, columnspan=2, pady=15)  # ปุ่มสมัครสมาชิก

# --- ส่วนของ dashboard ---
def open_dashboard(root, farm_number):  # ฟังก์ชันเปิดหน้าต่าง Dashboard
    dash_win = tk.Toplevel(root)  # สร้างหน้าต่างใหม่
    dash_win.title(f"Dashboard ฟาร์ม {farm_number}")  # ตั้งชื่อหน้าต่าง
    dash_win.geometry("400x300")  # กำหนดขนาดหน้าต่าง

    tk.Label(dash_win, text=f"ยินดีต้อนรับสู่ Dashboard ฟาร์ม {farm_number}", font=("Tahoma", 16)).pack(pady=30)  # ข้อความต้อนรับ
    widget_frame = tk.Frame(dash_win)  # สร้างเฟรมสำหรับวาง widget อื่นๆ
    widget_frame.pack(pady=20)

# --- ส่วนของ main ---
def open_farm_window():  # ฟังก์ชันเปิดหน้าต่างเลือกฟาร์ม
    farm_win = tk.Toplevel(root)  # สร้างหน้าต่างใหม่
    farm_win.title("Minifarm (โครงการ) เลือกฟาร์ม")  # ตั้งชื่อหน้าต่าง
    farm_win.geometry("500x300")  # กำหนดขนาดหน้าต่าง

    tk.Label(farm_win, text="Minifarm (โครงการ) เลือกฟาร์ม", font=("Tahoma", 16)).pack(pady=10)  # ข้อความหัวข้อ

    farm_frame = tk.Frame(farm_win)  # สร้างเฟรมสำหรับวางกล่องฟาร์ม
    farm_frame.pack(pady=20)

    farm_var = tk.IntVar(value=1)  # ตัวแปรเก็บค่าฟาร์มที่เลือก

    for i in range(1, 4):  # สร้างกล่องเลือกฟาร์ม 3 กล่อง
        box = tk.Frame(farm_frame, width=80, height=80, highlightbackground="blue", highlightthickness=2)
        box.grid(row=0, column=i-1, padx=20)
        box.pack_propagate(False)
        tk.Label(box, text=str(i), font=("Tahoma", 32), fg="blue").pack(expand=True)
        tk.Radiobutton(farm_frame, value=i, variable=farm_var).grid(row=1, column=i-1)

    def next_action():  # ฟังก์ชันเมื่อกดปุ่ม Next
        selected = farm_var.get()  # อ่านค่าฟาร์มที่เลือก
        farm_win.destroy()  # ปิดหน้าต่างเลือกฟาร์ม
        open_dashboard(root, selected)  # เปิด Dashboard ของฟาร์มที่เลือก
        tk.messagebox.showinfo("เลือกฟาร์ม", f"คุณเลือกฟาร์มหมายเลข {selected}")

    tk.Button(farm_win, text="Next", font=("Tahoma", 14), width=10, command=next_action).pack(pady=10)  # ปุ่ม Next

def login():  # ฟังก์ชันตรวจสอบการเข้าสู่ระบบ
    username = entry_username.get()  # รับค่าจากช่องกรอก Username
    password = entry_password.get()  # รับค่าจากช่องกรอก Password
    if username in users and users[username] == password:  # ตรวจสอบ Username และ Password
        messagebox.showinfo("ผลลัพธ์", "Login สำเร็จ!")
        open_farm_window()  # เปิดหน้าต่างเลือกฟาร์ม
    else:
        messagebox.showerror("ผลลัพธ์", "Login ไม่สำเร็จ กรุณาตรวจสอบข้อมูลอีกครั้ง")

root = tk.Tk()  # สร้างหน้าต่างหลัก
root.title("Login App")  # ตั้งชื่อหน้าต่างหลัก
root.geometry("500x500")  # กำหนดขนาดหน้าต่างหลัก

frame = tk.Frame(root, padx=20, pady=20)  # สร้างเฟรมสำหรับวาง widget
frame.pack(expand=True)

tk.Label(frame, text="Username:").grid(row=0, column=0, sticky="e", pady=5)  # ป้ายชื่อ Username
entry_username = tk.Entry(frame)  # ช่องกรอก Username
entry_username.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Password:").grid(row=1, column=0, sticky="e", pady=5)  # ป้ายชื่อ Password
entry_password = tk.Entry(frame, show="*")  # ช่องกรอก Password (ซ่อนตัวอักษร)
entry_password.grid(row=1, column=1, pady=5)

tk.Button(frame, text="Login", command=login, width=15).grid(row=2, column=0, columnspan=2, pady=5)  # ปุ่ม Login
tk.Button(frame, text="สมัครสมาชิก", command=lambda: open_register(root), width=15).grid(row=3, columnspan=2, pady=5)  # ปุ่มสมัครสมาชิก
root.mainloop()  # เริ่มลูปหลักของโปรแกรม