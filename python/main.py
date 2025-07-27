import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, auth
import os # Import os module for path operations

# --- Firebase Configuration (Client-side) ---
# สำหรับ firebase-admin เราจะใช้ Service Account Key
# ดาวน์โหลดไฟล์ .json จาก Firebase Console -> Project settings -> Service accounts -> Generate new private key
# และวางไฟล์นี้ไว้ในโฟลเดอร์เดียวกับ main.py
SERVICE_ACCOUNT_KEY_PATH = "my-small-farm-system-firebase-adminsdk-fbsvc-343c1b46e5.json" # <-- เปลี่ยนชื่อไฟล์นี้ให้ตรงกับของคุณแล้ว!

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

    # --- Register Screen ---
    def show_register_screen(self):
        self.clear_frame()
        self.title("สมัครสมาชิก - ระบบจัดการฟาร์ม")

        register_card = tk.Frame(self.main_frame, bg="white", bd=2, relief="flat", padx=30, pady=30)
        register_card.pack(pady=50, padx=50)

        tk.Label(register_card, text="ระบบจัดการฟาร์ม", font=("Inter", 28, "bold"), fg="#333333", bg="white").pack(pady=(0, 10))
        tk.Label(register_card, text="เข้าสู่โลกแห่งการเกษตรยุคใหม่", font=("Inter", 14), fg="#666666", bg="white").pack(pady=(0, 20))

        tk.Label(register_card, text="สมัครสมาชิก", font=self.heading_font, fg=self.text_color, bg="white").pack(pady=(0, 20))

        # Email Input
        tk.Label(register_card, text="อีเมล:", font=self.default_font, fg=self.text_color, bg="white").pack(anchor="w", pady=(10, 0))
        self.reg_email_entry = tk.Entry(register_card, font=self.default_font, width=40, bd=2, relief="groove", highlightbackground="#cccccc", highlightthickness=1)
        self.reg_email_entry.pack(pady=(0, 10))

        # Password Input
        tk.Label(register_card, text="รหัสผ่าน:", font=self.default_font, fg=self.text_color, bg="white").pack(anchor="w", pady=(10, 0))
        self.reg_password_entry = tk.Entry(register_card, font=self.default_font, show="*", width=40, bd=2, relief="groove", highlightbackground="#cccccc", highlightthickness=1)
        self.reg_password_entry.pack(pady=(0, 10))

        # Confirm Password Input
        tk.Label(register_card, text="ยืนยันรหัสผ่าน:", font=self.default_font, fg=self.text_color, bg="white").pack(anchor="w", pady=(10, 0))
        self.confirm_password_entry = tk.Entry(register_card, font=self.default_font, show="*", width=40, bd=2, relief="groove", highlightbackground="#cccccc", highlightthickness=1)
        self.confirm_password_entry.pack(pady=(0, 20))

        # Register Button
        register_button = tk.Button(register_card, text="สมัครสมาชิก", font=self.button_font, bg=self.primary_color, fg="white",
                                    command=self.register_user, width=30, height=2, relief="raised", bd=2)
        register_button.pack(pady=(10, 10))

        # Login Link
        login_frame = tk.Frame(register_card, bg="white")
        login_frame.pack(pady=(10, 0))
        tk.Label(login_frame, text="มีบัญชีอยู่แล้วใช่ไหม?", font=self.default_font, fg=self.primary_color, bg="white", bd=0).pack(side="left")
        tk.Button(login_frame, text="เข้าสู่ระบบ", font=self.default_font, fg=self.primary_color, bg="white", bd=0,
                  command=self.show_login_screen, cursor="hand2").pack(side="left", padx=5)

    def register_user(self):
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not email or not password or not confirm_password:
            messagebox.showwarning("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบถ้วนทุกช่อง")
            return
        if password != confirm_password:
            messagebox.showwarning("ข้อผิดพลาด", "รหัสผ่านและการยืนยันรหัสผ่านไม่ตรงกัน")
            return
        if len(password) < 6:
            messagebox.showwarning("ข้อผิดพลาด", "รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร")
            return

        try:
            # การสมัครสมาชิกด้วย Firebase Admin SDK
            user = auth.create_user(email=email, password=password)
            # ในโปรเจกต์จริง อาจจะบันทึกข้อมูลผู้ใช้เพิ่มเติมลง Firestore/Realtime DB ที่นี่
            # db.child("users").child(user['localId']).set({"email": email, "role": "member"})

            messagebox.showinfo("สำเร็จ", f"สมัครสมาชิกสำเร็จ! ยินดีต้อนรับ {email}")
            self.show_login_screen()

        except auth.AuthError as e:
            error_message = str(e)
            if e.code == 'auth/email-already-exists':
                messagebox.showerror("สมัครสมาชิกไม่สำเร็จ", "อีเมลนี้ถูกใช้ไปแล้ว")
            elif e.code == 'auth/weak-password':
                messagebox.showerror("สมัครสมาชิกไม่สำเร็จ", "รหัสผ่านอ่อนเกินไป กรุณาใช้รหัสผ่านที่ซับซ้อนกว่านี้")
            else:
                messagebox.showerror("สมัครสมาชิกไม่สำเร็จ", f"เกิดข้อผิดพลาด: {e.code}")
            print(f"Register Error (Firebase Admin): {e}")
        except Exception as e:
            messagebox.showerror("สมัครสมาชิกไม่สำเร็จ", f"เกิดข้อผิดพลาด: {e}")
            print(f"Register Error (General): {e}")

    # --- Farm Selection Screen ---
    def show_farm_selection_screen(self):
        # ตรวจสอบว่าผู้ใช้ Login อยู่หรือไม่
        # ใน firebase-admin, auth.current_user ไม่มีอยู่
        # คุณต้องใช้ auth.get_user(uid) หรือ auth.verify_id_token(id_token)
        # แต่ใน Desktop App ที่ไม่มีการจัดการ Session แบบ Web/Mobile
        # เราจะถือว่าถ้า self.current_user มีค่า ก็คือ Login อยู่
        if not self.current_user:
            messagebox.showwarning("เข้าสู่ระบบ", "กรุณาเข้าสู่ระบบก่อน")
            self.show_login_screen()
            return

        self.clear_frame()
        self.title("Minifarm - เลือกฟาร์ม")

        header_frame = tk.Frame(self.main_frame, bg="#E8F5E9")
        header_frame.pack(fill="x", pady=20, padx=40)
        tk.Label(header_frame, text="Minifarm", font=("Inter", 28, "bold"), fg="#333333", bg="#E8F5E9").pack(side="left")
        logout_button = tk.Button(header_frame, text="ออกจากระบบ", font=self.button_font, bg=self.secondary_color, fg="white",
                                  command=self.logout_user, relief="raised", bd=2)
        logout_button.pack(side="right")

        farm_selection_card = tk.Frame(self.main_frame, bg="white", bd=2, relief="flat", padx=30, pady=30)
        farm_selection_card.pack(pady=20, padx=50)

        tk.Label(farm_selection_card, text="เลือกฟาร์มของคุณ", font=self.heading_font, fg=self.text_color, bg="white").pack(pady=(0, 20))

        # Farm Cards Container (using grid for layout)
        farm_cards_frame = tk.Frame(farm_selection_card, bg="white")
        farm_cards_frame.pack(pady=(0, 20))

        self.farm_cards = []
        # Example farms - In a real app, these would be fetched from Firebase Firestore/Realtime DB
        # สำหรับโปรเจกต์นี้ คุณจะต้องเชื่อมต่อกับ Firestore เพื่อดึงข้อมูลฟาร์มจริง
        # และจัดการการสร้าง/เข้าร่วมฟาร์ม
        farms_data = [
            {"id": "farm1", "name": "ฟาร์มที่ 1", "description": "สวนผักอินทรีย์"},
            {"id": "farm2", "name": "ฟาร์มที่ 2", "description": "ไร่ผลไม้รวม"},
            {"id": "farm3", "name": "ฟาร์mที่ 3", "description": "บ่อปลาอัจฉริยะ"},
        ]

        for i, farm in enumerate(farms_data):
            # สร้าง Frame สำหรับแต่ละการ์ดฟาร์ม
            card = tk.Frame(farm_cards_frame, bg="#F8FDF8", bd=1, relief="solid", highlightbackground="#B2DFDB", highlightthickness=1, padx=20, pady=20)
            card.grid(row=i // 3, column=i % 3, padx=10, pady=10) # จัดเรียง 3 คอลัมน์ต่อแถว
            
            # ผูก Event Click ให้กับการ์ด
            # ใช้ lambda เพื่อส่ง farm_id ไปด้วย
            card.bind("<Button-1>", lambda e, f_id=farm["id"], current_card=card: self.on_farm_card_click(current_card, f_id))
            
            # เพิ่ม Label ภายใน Frame การ์ด
            tk.Label(card, text=farm["name"], font=self.subheading_font, fg="#4CAF50", bg="#F8FDF8").pack(pady=(0, 5))
            tk.Label(card, text=farm["description"], font=self.default_font, fg="#666666", bg="#F8FDF8").pack()

            self.farm_cards.append(card)

        self.next_button = tk.Button(farm_selection_card, text="ดำเนินการต่อ", font=self.button_font, bg=self.primary_color, fg="white",
                                     command=self.proceed_to_dashboard, width=30, height=2, relief="raised", bd=2, state=tk.DISABLED)
        self.next_button.pack(pady=(10, 10))

    def on_farm_card_click(self, clicked_card, farm_id):
        # ลบ 'selected' styling ออกจากการ์ดทั้งหมด
        for card in self.farm_cards:
            card.config(highlightbackground="#B2DFDB", highlightthickness=1)
        
        # เพิ่ม 'selected' styling ให้กับการ์ดที่ถูกคลิก
        clicked_card.config(highlightbackground="#4CAF50", highlightthickness=3)
        self.selected_farm_id = farm_id
        self.next_button.config(state=tk.NORMAL) # เปิดใช้งานปุ่มดำเนินการต่อ

    def proceed_to_dashboard(self):
        if self.selected_farm_id:
            messagebox.showinfo("เลือกฟาร์ม", f"คุณได้เลือก {self.selected_farm_id} แล้ว!")
            self.show_dashboard_screen(self.selected_farm_id)
        else:
            messagebox.showwarning("ข้อผิดพลาด", "กรุณาเลือกฟาร์มก่อนดำเนินการต่อ")

    def logout_user(self):
        # ใน firebase-admin ไม่มีเมธอด sign_out() โดยตรงสำหรับ Client-side
        # การออกจากระบบใน Desktop App ที่ใช้ Admin SDK คือการล้างสถานะผู้ใช้ในแอปพลิเคชัน
        self.current_user = None
        self.selected_farm_id = None
        messagebox.showinfo("ออกจากระบบ", "ออกจากระบบสำเร็จ")
        self.show_login_screen()

    # --- Dashboard Screen ---
    def show_dashboard_screen(self, farm_id):
        self.clear_frame()
        self.title(f"Minifarm - แดชบอร์ดฟาร์ม: {farm_id.upper()}")

        header_frame = tk.Frame(self.main_frame, bg="#E8F5E9")
        header_frame.pack(fill="x", pady=20, padx=40)
        tk.Label(header_frame, text="Minifarm Dashboard", font=("Inter", 28, "bold"), fg="#333333", bg="#E8F5E9").pack(side="left")
        
        button_group = tk.Frame(header_frame, bg="#E8F5E9")
        button_group.pack(side="right")

        back_button = tk.Button(button_group, text="เลือกฟาร์ม", font=self.button_font, bg=self.primary_color, fg="white",
                                command=self.show_farm_selection_screen, relief="raised", bd=2)
        back_button.pack(side="left", padx=5)

        logout_button = tk.Button(button_group, text="ออกจากระบบ", font=self.button_font, bg=self.secondary_color, fg="white",
                                  command=self.logout_user, relief="raised", bd=2)
        logout_button.pack(side="left", padx=5)

        dashboard_card = tk.Frame(self.main_frame, bg="white", bd=2, relief="flat", padx=30, pady=30)
        dashboard_card.pack(pady=20, padx=50)

        tk.Label(dashboard_card, text=f"ภาพรวมฟาร์ม: {farm_id.upper()}", font=self.heading_font, fg=self.text_color, bg="white").pack(pady=(0, 10))
        tk.Label(dashboard_card, text="ยินดีต้อนรับสู่แดชบอร์ดการจัดการฟาร์มของคุณ!", font=self.default_font, fg="#666666", bg="white").pack(pady=(0, 20))

        # Placeholder for dashboard content (similar to HTML version)
        # ในโปรเจกต์จริง ส่วนนี้จะดึงข้อมูลจาก Firestore/Realtime DB
        tk.Label(dashboard_card, text="จำนวนพืช: 120", font=self.subheading_font, fg=self.primary_color, bg="white").pack(pady=5)
        tk.Label(dashboard_card, text="จำนวนสัตว์: 35", font=self.subheading_font, fg="#FFC107", bg="white").pack(pady=5)
        tk.Label(dashboard_card, text="กิจกรรมวันนี้: 3", font=self.subheading_font, fg="#2196F3", bg="white").pack(pady=5)
        tk.Label(dashboard_card, text="ผลผลิตล่าสุด: 50 kg มะเขือเทศ", font=self.subheading_font, fg="#F44336", bg="white").pack(pady=5)

        tk.Label(dashboard_card, text="\nส่วนการจัดการ (กำลังพัฒนา...)", font=self.subheading_font, fg=self.text_color, bg="white").pack(pady=(20, 10))
        tk.Button(dashboard_card, text="จัดการพืช", font=self.button_font, bg="#E0F2F1", fg="#2e7d32", width=20, relief="groove").pack(pady=5)
        tk.Button(dashboard_card, text="จัดการสัตว์", font=self.button_font, bg="#FFF8E1", fg="#FFC107", width=20, relief="groove").pack(pady=5)
        tk.Button(dashboard_card, text="กิจกรรมและผลผลิต", font=self.button_font, bg="#E3F2FD", fg="#2196F3", width=20, relief="groove").pack(pady=5)
        tk.Button(dashboard_card, text="จัดการสมาชิก", font=self.button_font, bg="#EDE7F6", fg="#673AB7", width=20, relief="groove").pack(pady=5)


if __name__ == "__main__":
    app = FarmApp()
    app.mainloop()