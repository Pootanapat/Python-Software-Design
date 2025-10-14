import tkinter as tk
from tkinter import messagebox
from firebase_config import db
from utils import add_log

class InviteMemberScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title_label = tk.Label(self.frame, text="Invite Member", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=20)

        # คำอธิบาย
        desc_label = tk.Label(self.frame, text="Enter the email of the person you want to invite to this farm.", font=("Arial", 11), bg="#f5f5f5", fg="#7f8c8d")
        desc_label.pack(pady=5)

        # ช่องกรอกอีเมล
        tk.Label(self.frame, text="Email", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(10, 2))
        self.email_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
        self.email_entry.pack(pady=5)

        # ปุ่ม Invite
        invite_btn = tk.Button(self.frame, text="📧 Invite", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", relief="flat", width=15, command=self.invite_member)
        invite_btn.pack(pady=20)
        invite_btn.bind("<Enter>", lambda e: invite_btn.config(bg="#27ae60"))
        invite_btn.bind("<Leave>", lambda e: invite_btn.config(bg="#2ecc71"))

        # ปุ่ม Back
        back_btn = tk.Button(self.frame, text="← Back", font=("Arial", 10, "bold"), bg="#95a5a6", fg="white", relief="flat", width=10, command=self.go_back)
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#7f8c8d"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#95a5a6"))

    def invite_member(self):
        email = self.email_entry.get()
        if not email:
            messagebox.showwarning("Warning", "Please enter an email.")
            return

        try:
            # เพิ่มอีเมลลงใน invites ของฟาร์ม
            db.child("farms").child(self.app.current_farm).child("invites").push({
                "email": email,
                "role": "pending"
            })
            add_log(self.app.current_farm, self.app.current_user['localId'], "invited_member", {"email": email})
            messagebox.showinfo("Success", f"Invitation sent to {email} successfully!")
            self.go_back()
        except Exception as e:
            messagebox.showerror("Error", f"Could not send invite: {str(e)}")

    def go_back(self):
        self.app.clear_window()
        from screens.manager_screen import ManagerScreen
        ManagerScreen(self.app)