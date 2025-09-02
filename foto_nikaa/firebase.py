import tkinter as tk
from tkinter import ttk, messagebox

# ==== ติดตั้งไลบรารีที่จำเป็นก่อนรันโปรแกรม ====
# pip install pyrebase4 requests

firebaseConfig = {
  "apiKey": "AIzaSyCHOMHm_XTE1_-oZVloRudi7Fxhs2Ygu_U",
  "authDomain": "my-small-farm-system.firebaseapp.com",
  "databaseURL": "https://my-small-farm-system-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "my-small-farm-system",
  "storageBucket": "my-small-farm-system.firebasestorage.app",
  "messagingSenderId": "214056545877",
  "appId": "1:214056545877:web:ff1b28273d8f65e70c2edc"
}

REQUIRED_KEYS = ["apiKey", "authDomain", "projectId", "appId"]

try:
    import pyrebase
except Exception as e:
    raise SystemExit("\nโปรดติดตั้ง pyrebase4 ก่อน: pip install pyrebase4\nรายละเอียด: " + str(e))


def ensure_firebase_config(cfg: dict) -> None:
    missing = [k for k in REQUIRED_KEYS if not cfg.get(k) or "PASTE" in str(cfg.get(k)) or "your-project-id" in str(cfg.get(k))]
    if missing:
        raise SystemExit(
            "\n[Config Error] โปรดแก้ไขค่า firebaseConfig ให้ถูกต้องในสคริปต์นี้ก่อนรันต่อ: " + ", ".join(missing)
        )


class MiniFarmAuthApp(tk.Tk):
    """แอปตัวอย่าง MiniFarm เฉพาะหน้า Login/Register ด้วย Firebase (Email/Password)"""

    def __init__(self, firebase_app):
        super().__init__()
        self.title("MiniFarm | Login & Register")
        self.geometry("460x420")
        self.resizable(False, False)

        self.firebase = firebase_app
        self.auth = self.firebase.auth()

        style = ttk.Style(self)
        style.configure("TButton", padding=8)
        style.configure("TEntry", padding=6)
        style.configure("TLabel", padding=4)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=12, pady=12)

        self.login_frame = ttk.Frame(self.nb)
        self.register_frame = ttk.Frame(self.nb)

        self.nb.add(self.login_frame, text="Login")
        self.nb.add(self.register_frame, text="Register")

        self._build_login_ui()
        self._build_register_ui()

    def _build_login_ui(self):
        wrapper = ttk.Frame(self.login_frame, padding=12)
        wrapper.pack(fill="both", expand=True)

        ttk.Label(wrapper, text="เข้าสู่ระบบ", font=("Segoe UI", 16, "bold")).pack(pady=(8, 12))

        self.login_email_var = tk.StringVar()
        self.login_password_var = tk.StringVar()

        email_row = ttk.Frame(wrapper)
        email_row.pack(fill="x", pady=6)
        ttk.Label(email_row, text="อีเมล").pack(anchor="w")
        ttk.Entry(email_row, textvariable=self.login_email_var).pack(fill="x")

        pass_row = ttk.Frame(wrapper)
        pass_row.pack(fill="x", pady=6)
        ttk.Label(pass_row, text="รหัสผ่าน").pack(anchor="w")
        ttk.Entry(pass_row, textvariable=self.login_password_var, show="•").pack(fill="x")

        btn_row = ttk.Frame(wrapper)
        btn_row.pack(fill="x", pady=14)

        ttk.Button(btn_row, text="เข้าสู่ระบบ", command=self.on_login).pack(side="left")
        ttk.Button(btn_row, text="ไปที่ Register", command=lambda: self.nb.select(self.register_frame)).pack(side="right")

    def _build_register_ui(self):
        wrapper = ttk.Frame(self.register_frame, padding=12)
        wrapper.pack(fill="both", expand=True)

        ttk.Label(wrapper, text="สมัครสมาชิก", font=("Segoe UI", 16, "bold")).pack(pady=(8, 12))

        self.reg_email_var = tk.StringVar()
        self.reg_password_var = tk.StringVar()
        self.reg_confirm_var = tk.StringVar()

        email_row = ttk.Frame(wrapper)
        email_row.pack(fill="x", pady=6)
        ttk.Label(email_row, text="อีเมล").pack(anchor="w")
        ttk.Entry(email_row, textvariable=self.reg_email_var).pack(fill="x")

        pass_row = ttk.Frame(wrapper)
        pass_row.pack(fill="x", pady=6)
        ttk.Label(pass_row, text="รหัสผ่าน (อย่างน้อย 6 ตัวอักษร)").pack(anchor="w")
        ttk.Entry(pass_row, textvariable=self.reg_password_var, show="•").pack(fill="x")

        confirm_row = ttk.Frame(wrapper)
        confirm_row.pack(fill="x", pady=6)
        ttk.Label(confirm_row, text="ยืนยันรหัสผ่าน").pack(anchor="w")
        ttk.Entry(confirm_row, textvariable=self.reg_confirm_var, show="•").pack(fill="x")

        btn_row = ttk.Frame(wrapper)
        btn_row.pack(fill="x", pady=14)

        ttk.Button(btn_row, text="สมัครสมาชิก", command=self.on_register).pack(side="left")
        ttk.Button(btn_row, text="ไปที่ Login", command=lambda: self.nb.select(self.login_frame)).pack(side="right")

    def on_login(self):
        email = self.login_email_var.get().strip()
        password = self.login_password_var.get()

        if not email or not password:
            messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอกอีเมลและรหัสผ่าน")
            return

        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            id_token = user.get("idToken")
            local_id = user.get("localId")

            self.destroy()  # ปิดหน้า Login หลัก
            MainApp(email=email, uid=local_id, id_token=id_token).mainloop()
        except Exception as e:
            msg = parse_pyrebase_error(e)
            messagebox.showerror("เข้าสู่ระบบไม่สำเร็จ", msg)

    def on_register(self):
        email = self.reg_email_var.get().strip()
        password = self.reg_password_var.get()
        confirm = self.reg_confirm_var.get()

        if not email or not password:
            messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอกอีเมลและรหัสผ่านให้ครบถ้วน")
            return
        if password != confirm:
            messagebox.showwarning("ไม่ตรงกัน", "รหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน")
            return
        if len(password) < 6:
            messagebox.showwarning("รหัสผ่านสั้นเกินไป", "รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร")
            return

        try:
            user = self.auth.create_user_with_email_and_password(email, password)
            uid = user.get("localId")
            messagebox.showinfo("สมัครสมาชิกสำเร็จ", f"สร้างบัญชีสำเร็จ\nUID: {uid}\nคุณสามารถเข้าสู่ระบบได้แล้ว")
            self.nb.select(self.login_frame)
        except Exception as e:
            msg = parse_pyrebase_error(e)
            messagebox.showerror("สมัครสมาชิกไม่สำเร็จ", msg)


class MainApp(tk.Tk):
    def __init__(self, email: str, uid: str, id_token: str):
        super().__init__()
        self.title("MiniFarm | Main")
        self.geometry("600x400")
        self.resizable(False, False)

        ttk.Label(self, text="MiniFarm Main Page", font=("Segoe UI", 18, "bold")).pack(pady=20)
        ttk.Label(self, text=f"สวัสดีคุณ {email}").pack(pady=5)
        ttk.Label(self, text=f"UID: {uid}").pack(pady=5)

        ttk.Button(self, text="ออกจากระบบ", command=self.quit).pack(pady=20)


# ---------------- Helper: แปลงข้อความ error -----------------
def parse_pyrebase_error(e: Exception) -> str:
    import json
    default_msg = f"เกิดข้อผิดพลาด: {e}"
    try:
        if hasattr(e, "args") and len(e.args) > 1:
            data = e.args[1]
            if isinstance(data, (bytes, bytearray)):
                data = data.decode("utf-8", errors="ignore")
            j = json.loads(data)
            err = (j.get("error") or {}).get("message")
            if err:
                mapping = {
                    "EMAIL_NOT_FOUND": "ไม่พบบัญชีผู้ใช้นี้",
                    "INVALID_PASSWORD": "รหัสผ่านไม่ถูกต้อง",
                    "USER_DISABLED": "บัญชีถูกปิดการใช้งาน",
                    "EMAIL_EXISTS": "อีเมลนี้ถูกใช้แล้ว",
                }
                return mapping.get(err, err)
    except Exception:
        pass
    return default_msg


if __name__ == "__main__":
    ensure_firebase_config(firebaseConfig)
    firebase_app = pyrebase.initialize_app(firebaseConfig)
    app = MiniFarmAuthApp(firebase_app)
    app.mainloop()
