import tkinter as tk
from tkinter import messagebox
from register import open_register, users  # นำเข้า open_register และ users
from dashboard import open_dashboard
def open_farm_window():
    farm_win = tk.Toplevel(root)
    farm_win.title("Minifarm (โครงการ) เลือกฟาร์ม")
    farm_win.geometry("500x300")

    tk.Label(farm_win, text="Minifarm (โครงการ) เลือกฟาร์ม", font=("Tahoma", 16)).pack(pady=10)

    farm_frame = tk.Frame(farm_win)
    farm_frame.pack(pady=20)

    farm_var = tk.IntVar(value=1)  # ประกาศตัวแปรในนี้ก็ได้

    for i in range(1, 4):
        box = tk.Frame(farm_frame, width=80, height=80, highlightbackground="blue", highlightthickness=2)
        box.grid(row=0, column=i-1, padx=20)
        box.pack_propagate(False)
        tk.Label(box, text=str(i), font=("Tahoma", 32), fg="blue").pack(expand=True)
        tk.Radiobutton(farm_frame, value=i, variable=farm_var).grid(row=1, column=i-1)

    def next_action():
        selected = farm_var.get()
        farm_win.destroy()  # ปิดหน้าต่างเลือกฟาร์ม
        open_dashboard(root, selected)  # เปิด dashboard
        tk.messagebox.showinfo("เลือกฟาร์ม", f"คุณเลือกฟาร์มหมายเลข {selected}")

    tk.Button(farm_win, text="Next", font=("Tahoma", 14), width=10, command=next_action).pack(pady=10)
def login():
    username = entry_username.get()
    password = entry_password.get()
    if username in users and users[username] == password:
        messagebox.showinfo("ผลลัพธ์", "Login สำเร็จ!")
        open_farm_window()
    else:
        messagebox.showerror("ผลลัพธ์", "Login ไม่สำเร็จ กรุณาตรวจสอบข้อมูลอีกครั้ง")

root = tk.Tk()
root.title("Login App")
root.geometry("500x500")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

tk.Label(frame, text="Username:").grid(row=0, column=0, sticky="e", pady=5)
entry_username = tk.Entry(frame)
entry_username.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Password:").grid(row=1, column=0, sticky="e", pady=5)
entry_password = tk.Entry(frame, show="*")
entry_password.grid(row=1, column=1, pady=5)

tk.Button(frame, text="Login", command=login, width=15).grid(row=2, column=0, columnspan=2, pady=5)
tk.Button(frame, text="สมัครสมาชิก", command=lambda: open_register(root), width=15).grid(row=3, column=0, columnspan=2, pady=5)

farm_var = tk.IntVar(value=1)  # ตัวแปรสำหรับเลือกฟาร์ม

root.mainloop()