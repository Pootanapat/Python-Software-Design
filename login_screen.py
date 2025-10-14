import tkinter as tk
from tkinter import messagebox
from firebase_config import auth
from utils import add_log

class LoginScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title_label = tk.Label(self.frame, text="MINIFARM", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title_label.pack(pady=30)

        subtitle_label = tk.Label(self.frame, text="Login", font=("Arial", 16), bg="#f0f0f0", fg="#7f8c8d")
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

        # ปุ่ม Login
        login_btn = tk.Button(self.frame, text="Login", font=("Arial", 12, "bold"), bg="#3498db", fg="white", relief="flat", width=20, height=2, command=self.login)
        login_btn.pack(pady=20)
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#2980b9"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#3498db"))

        # ปุ่ม Sign Up
        signup_btn = tk.Button(self.frame, text="Don't have an account? Sign Up", font=("Arial", 10), bg="#f0f0f0", fg="#3498db", relief="flat", command=self.go_to_signup)
        signup_btn.pack(pady=10)
        signup_btn.bind("<Enter>", lambda e: signup_btn.config(bg="#e0e0e0"))
        signup_btn.bind("<Leave>", lambda e: signup_btn.config(bg="#f0f0f0"))

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if not email or not password:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            self.app.current_user = user
            add_log(None, user['localId'], "login", {"email": email})
            from screens.farm_selection_screen import FarmSelectionScreen
            self.app.clear_window()
            FarmSelectionScreen(self.app)
        except Exception as e:
            messagebox.showerror("Error", "Email หรือ Password ไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง")

    def go_to_signup(self):
        self.app.clear_window()
        from screens.signup_screen import SignUpScreen
        SignUpScreen(self.app)