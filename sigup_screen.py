import tkinter as tk
from tkinter import messagebox
from firebase_config import auth
from utils import add_log

class SignUpScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title_label = tk.Label(self.frame, text="MINIFARM", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title_label.pack(pady=30)

        subtitle_label = tk.Label(self.frame, text="Sign Up", font=("Arial", 16), bg="#f0f0f0", fg="#7f8c8d")
        subtitle_label.pack(pady=10)

        # ช่องกรอกอีเมล
        email_label = tk.Label(self.frame, text="Email", font=("Arial", 12), bg="#f0f0f0", fg="#2c3e50")
        email_label.pack(pady=(10, 5))
        self.email_entry = tk.Entry(self.frame, font=("Arial", 12), width=30, relief="solid", bd=1)
        self.email_entry.pack(pady=5)

        # ช่องกรอกรหัสผ่าน
        password_label = tk.Label(self.frame, text="Password", font=("Arial", 12), bg="#f0f0f0", fg="#2c3e50")
        password_label.pack(pady=(10, 5))
        self.password_entry = tk.Entry(self.frame, font=("Arial", 12), width=30, relief="solid", bd=1, show="*")
        self.password_entry.pack(pady=5)

        # ช่องยืนยันรหัสผ่าน
        confirm_password_label = tk.Label(self.frame, text="Confirm Password", font=("Arial", 12), bg="#f0f0f0", fg="#2c3e50")
        confirm_password_label.pack(pady=(10, 5))
        self.confirm_password_entry = tk.Entry(self.frame, font=("Arial", 12), width=30, relief="solid", bd=1, show="*")
        self.confirm_password_entry.pack(pady=5)

        # ปุ่ม Sign Up
        signup_btn = tk.Button(self.frame, text="Sign Up", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", relief="flat", width=20, height=2, command=self.signup)
        signup_btn.pack(pady=20)
        signup_btn.bind("<Enter>", lambda e: signup_btn.config(bg="#27ae60"))
        signup_btn.bind("<Leave>", lambda e: signup_btn.config(bg="#2ecc71"))

        # ปุ่มกลับไป Login
        back_btn = tk.Button(self.frame, text="← Back to Login", font=("Arial", 10), bg="#f0f0f0", fg="#3498db", relief="flat", command=self.go_to_login)
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#e0e0e0"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#f0f0f0"))

    def signup(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not email or not password or not confirm_password:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Password ไม่ตรงกัน กรุณากรอกใหม่อีกครั้ง")
            return

        try:
            user = auth.create_user_with_email_and_password(email, password)
            add_log(None, user['localId'], "signup", {"email": email})
            messagebox.showinfo("Success", "Account created successfully!")
            self.go_to_login()
        except Exception as e:
            messagebox.showerror("Error", f"Signup failed: {str(e)}")

    def go_to_login(self):
        self.app.clear_window()
        from screens.login_screen import LoginScreen
        LoginScreen(self.app)