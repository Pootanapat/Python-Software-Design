import tkinter as tk
from tkinter import messagebox

users = {
    "admin": "1234",
    "user": "abcd"
}

def open_register(root):
    reg_win = tk.Toplevel(root)
    reg_win.title("สมัครสมาชิก")
    reg_win.geometry("300x180")

    tk.Label(reg_win, text="Username:").grid(row=0, column=0, pady=5, sticky="e")
    reg_username = tk.Entry(reg_win)
    reg_username.grid(row=0, column=1, pady=5)

    tk.Label(reg_win, text="Password:").grid(row=1, column=0, pady=5, sticky="e")
    reg_password = tk.Entry(reg_win, show="*")
    reg_password.grid(row=1, column=1, pady=5)

    def register():
        username = reg_username.get()
        password = reg_password.get()
        if username in users:
            messagebox.showerror("ผิดพลาด", "Username นี้มีอยู่แล้ว")
        elif not username or not password:
            messagebox.showerror("ผิดพลาด", "กรุณากรอกข้อมูลให้ครบ")
        else:
            users[username] = password
            messagebox.showinfo("สำเร็จ", "สมัครสมาชิกสำเร็จ!")
            reg_win.destroy()

    tk.Button(reg_win, text="สมัครสมาชิก", command=register, width=15).grid(row=2, column=0, columnspan=2, pady=15)