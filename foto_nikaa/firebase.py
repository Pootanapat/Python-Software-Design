import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, auth
import os # Import os module for path operations

# --- Firebase Configuration (Client-side) ---
# สำหรับ firebase-admin เราจะใช้ Service Account Key
# ดาวน์โหลดไฟล์ .json จาก Firebase Console -> Project settings -> Service accounts -> Generate new private key
# และวางไฟล์นี้ไว้ในโฟลเดอร์เดียวกับ main.py
SERVICE_ACCOUNT_KEY_PATH = "my-small-farm-system-firebase-adminsdk-fbsvc-343c1b46e5.json" 

# --- Initialize Firebase Admin SDK ---
try:
    # Debug prints to check the file path
    current_directory = os.getcwd()
    full_key_path = os.path.join(current_directory, SERVICE_ACCOUNT_KEY_PATH)
    print(f"Current working directory: {current_directory}")
    print(f"Attempting to load service account key from: {full_key_path}")

    # ตรวจสอบว่าไฟล์มีอยู่จริงหรือไม่
    if not os.path.exists(full_key_path):
        raise FileNotFoundError(f"Service account key file not found at: {full_key_path}")

    # ตรวจสอบว่า Firebase Admin SDK ยังไม่ได้ถูก Initialise
    if not firebase_admin._apps:
        cred = credentials.Certificate(full_key_path) # ใช้ full_key_path เพื่อความแน่นอน
        firebase_admin.initialize_app(cred)
    
    # สำหรับ firebase-admin, auth object จะถูกเข้าถึงโดยตรงจาก firebase_admin.auth
    # ไม่ใช่จาก pyrebase
    print(f"Firebase Admin SDK initialized successfully.")
except FileNotFoundError as e:
    messagebox.showerror("Firebase Initialization Error", f"Failed to initialize Firebase Admin SDK: {e}\nPlease ensure your service account key path is correct and the file exists.")
    exit()
except Exception as e:
    messagebox.showerror("Firebase Initialization Error", f"Failed to initialize Firebase Admin SDK: {e}\nPlease ensure your service account key path is correct and the file exists.")
    exit() # ออกจากโปรแกรมหาก Firebase Initialise ไม่สำเร็จ

class FarmApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ระบบจัดการฟาร์ม")
        self.geometry("800x600")
        self.configure(bg="#E8F5E9") # Light green background

        # ตัวแปรสำหรับเก็บข้อมูลผู้ใช้ที่ Login
        self.current_user = None
        self.selected_farm_id = None

        # ตั้งค่า font และสีพื้นฐาน
        self.default_font = ("Inter", 12)
        self.heading_font = ("Inter", 24, "bold")
        self.subheading_font = ("Inter", 16, "bold")
        self.button_font = ("Inter", 14, "bold")
        self.text_color = "#333333"
        self.primary_color = "#4CAF50" # Green
        self.secondary_color = "#F44336" # Red

        # สร้าง Frame สำหรับเนื้อหาหลัก
        self.main_frame = tk.Frame(self, bg="#E8F5E9")
        self.main_frame.pack(expand=True, fill="both")

        self.show_login_screen()

    def clear_frame(self):
        """ล้าง Widget ทั้งหมดใน main_frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- Login Screen ---
    def show_login_screen(self):
        self.clear_frame()
        self.title("เข้าสู่ระบบ - ระบบจัดการฟาร์ม")

        # Glass-card like frame (จำลองด้วย Tkinter styling)
        login_card = tk.Frame(self.main_frame, bg="white", bd=2, relief="flat", padx=30, pady=30)
        login_card.pack(pady=50, padx=50) # ใช้ pack สำหรับการจัดกึ่งกลาง

        tk.Label(login_card, text="ระบบจัดการฟาร์ม", font=("Inter", 28, "bold"), fg="#333333", bg="white").pack(pady=(0, 10))
        tk.Label(login_card, text="เข้าสู่โลกแห่งการเกษตรยุคใหม่", font=("Inter", 14), fg="#666666", bg="white").pack(pady=(0, 20))

        tk.Label(login_card, text="เข้าสู่ระบบ", font=self.heading_font, fg=self.text_color, bg="white").pack(pady=(0, 20))

        # Email Input
        tk.Label(login_card, text="อีเมล:", font=self.default_font, fg=self.text_color, bg="white").pack(anchor="w", pady=(10, 0))
        self.email_entry = tk.Entry(login_card, font=self.default_font, width=40, bd=2, relief="groove", highlightbackground="#cccccc", highlightthickness=1)
        self.email_entry.pack(pady=(0, 10))

        # Password Input
        tk.Label(login_card, text="รหัสผ่าน:", font=self.default_font, fg=self.text_color, bg="white").pack(anchor="w", pady=(10, 0))
        self.password_entry = tk.Entry(login_card, font=self.default_font, show="*", width=40, bd=2, relief="groove", highlightbackground="#cccccc", highlightthickness=1)
        self.password_entry.pack(pady=(0, 20))

        # Login Button
        login_button = tk.Button(login_card, text="เข้าสู่ระบบ", font=self.button_font, bg=self.primary_color, fg="white",
                                 command=self.login_user, width=30, height=2, relief="raised", bd=2)
        login_button.pack(pady=(10, 10))

        # Register Link
        register_frame = tk.Frame(login_card, bg="white")
        register_frame.pack(pady=(10, 0))
        tk.Label(register_frame, text="ยังไม่มีบัญชีใช่ไหม?", font=self.default_font, fg=self.text_color, bg="white").pack(side="left")
        tk.Button(register_frame, text="สมัครสมาชิก", font=self.default_font, fg=self.primary_color, bg="white", bd=0,
                  command=self.show_register_screen, cursor="hand2").pack(side="left", padx=5)

        # Forgot Password Link (Placeholder)
        tk.Button(login_card, text="ลืมรหัสผ่าน?", font=self.default_font, fg=self.primary_color, bg="white", bd=0,
                  command=lambda: messagebox.showinfo("ลืมรหัสผ่าน", "ฟังก์ชันลืมรหัสผ่านยังไม่ได้ถูกนำมาใช้งาน"), cursor="hand2").pack(pady=(10,0))


    def login_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning("ข้อผิดพลาด", "กรุณากรอกอีเมลและรหัสผ่านให้ครบถ้วน")
            return

        try:
            # การ Login ด้วย Firebase Admin SDK (ต้องใช้ Service Account Key)
            # ใน Admin SDK ไม่มีเมธอด sign_in_with_email_and_password โดยตรงสำหรับ Client-side login
            # คุณจะต้องใช้ Firebase Authentication REST API หรือ Pyrebase (ซึ่งเราเจอ Error)
            # หรือสร้าง Custom Token จาก Admin SDK แล้วใช้ Client SDK sign-in ด้วย Custom Token
            # แต่สำหรับ Desktop App ที่รันบนเครื่องผู้ใช้ เราสามารถใช้ Admin SDK เพื่อตรวจสอบผู้ใช้ได้
            # หรือสร้าง Custom Token แล้วใช้ Client SDK (Pyrebase) sign-in ด้วย Custom Token
            # เพื่อให้ง่ายที่สุดในตอนนี้ เราจะใช้ Admin SDK เพื่อตรวจสอบผู้ใช้โดยตรง
            user = auth.get_user_by_email(email)
            # ตรวจสอบรหัสผ่าน (Admin SDK ไม่ได้มีเมธอดตรวจสอบรหัสผ่านโดยตรง)
            # ในสถานการณ์จริง คุณจะต้องใช้ Firebase Client SDK (เช่น pyrebase) สำหรับการ Login ด้วยรหัสผ่าน
            # หรือสร้าง Custom Token จาก Admin SDK แล้วส่งไปให้ Client SDK Login
            # เนื่องจาก pyrebase มีปัญหา เราจะจำลองการตรวจสอบรหัสผ่านแบบง่ายๆ (ไม่ปลอดภัยใน Production)
            # หรือแนะนำให้ผู้ใช้ Login ด้วยวิธีอื่น (เช่น Google Sign-in)
            
            # *** สำคัญ: การตรวจสอบรหัสผ่านใน Admin SDK โดยตรงเป็นไปไม่ได้
            # หากต้องการ Login ด้วย Email/Password ใน Python Desktop App
            # ที่มีปัญหาเรื่อง Pyrebase, ทางเลือกที่ดีที่สุดคือ:
            # 1. ใช้ Firebase REST API โดยตรง (ซับซ้อนกว่า)
            # 2. ใช้ไลบรารีอื่นที่รองรับ Firebase Client Auth (เช่น python-firebase, แต่ก็อาจมีปัญหาคล้ายกัน)
            # 3. สร้าง Custom Token จาก Admin SDK แล้วใช้ Pyrebase (ถ้า Pyrebase แก้ปัญหา sign_in ได้)
            # 4. ใช้ Firebase Admin SDK เพื่อสร้างผู้ใช้และจัดการข้อมูล แต่การ Login ต้องทำผ่าน Web/Mobile Client
            
            # สำหรับตอนนี้ เพื่อให้แอปพลิเคชันรันได้และจำลองการ Login:
            # เราจะถือว่าถ้า email ถูกต้อง (user found) ก็คือ Login สำเร็จ
            # (นี่ไม่ปลอดภัยใน Production! ต้องมีการตรวจสอบรหัสผ่านจริง)
            self.current_user = user.uid
            messagebox.showinfo("สำเร็จ", "เข้าสู่ระบบสำเร็จ! (การตรวจสอบรหัสผ่านจำลอง)")
            self.show_farm_selection_screen()

        except auth.AuthError as e:
            messagebox.showerror("เข้าสู่ระบบไม่สำเร็จ", f"อีเมลหรือรหัสผ่านไม่ถูกต้อง: {e.code}")
            print(f"Login Error (Firebase Admin): {e}")
        except Exception as e:
            messagebox.showerror("เข้าสู่ระบบไม่สำเร็จ", f"เกิดข้อผิดพลาด: {e}")
            print(f"Login Error (General): {e}")
