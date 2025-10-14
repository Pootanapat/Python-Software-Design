import tkinter as tk
from tkinter import messagebox
from firebase_config import db
from utils import add_log

class JoinFarmScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title_label = tk.Label(self.frame, text="Join Farm", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=30)

        # คำอธิบาย
        desc_label = tk.Label(self.frame, text="Enter the email of the farm owner to join their farm.", font=("Arial", 10), bg="#f5f5f5", fg="#2c3e50")
        desc_label.pack(pady=5)

        # ช่องกรอกอีเมลเจ้าของฟาร์ม
        email_label = tk.Label(self.frame, text="Owner's Email", font=("Arial", 12), bg="#f5f5f5", fg="#2c3e50")
        email_label.pack(pady=(10, 5))
        self.email_entry = tk.Entry(self.frame, font=("Arial", 12), width=30, relief="solid", bd=1)
        self.email_entry.pack(pady=5)

        # ปุ่มเข้าร่วม
        join_btn = tk.Button(self.frame, text="Join Farm", font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", relief="flat", width=20, height=2, command=self.join_farm)
        join_btn.pack(pady=20)
        join_btn.bind("<Enter>", lambda e: join_btn.config(bg="#c0392b"))
        join_btn.bind("<Leave>", lambda e: join_btn.config(bg="#e74c3c"))

        # ปุ่มกลับ
        back_btn = tk.Button(self.frame, text="← Back", font=("Arial", 10, "bold"), bg="#95a5a6", fg="white", relief="flat", width=10, command=self.go_back)
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#7f8c8d"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#95a5a6"))

    def join_farm(self):
        owner_email = self.email_entry.get()
        if not owner_email:
            messagebox.showwarning("Warning", "Please enter the owner's email.")
            return

        try:
            users = db.child("users").get()
            owner_user_id = None
            for user in users.each():
                farms = db.child("users").child(user.key()).child("farms").get()
                if farms.each():
                    for farm in farms.each():
                        owner = db.child("farms").child(farm.key()).child("owner").get()
                        if owner.val() == user.key():
                            user_email = db.child("users").child(user.key()).child("email").get()
                            if user_email.val() == owner_email:
                                owner_user_id = user.key()
                                farm_id = farm.key()
                                break
            if owner_user_id:
                user_id = self.app.current_user['localId']
                db.child("farms").child(farm_id).child("members").child(user_id).set("pending")
                farm_name = db.child("farms").child(farm_id).child("name").get().val()
                db.child("users").child(user_id).child("farms").child(farm_id).set({"name": farm_name})
                add_log(farm_id, user_id, "joined_farm", {"by": owner_email})
                messagebox.showinfo("Success", "Successfully joined the farm!")
                self.go_back()
            else:
                messagebox.showerror("Error", "No farm found with that owner's email.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not join farm: {str(e)}")

    def go_back(self):
        self.app.clear_window()
        from screens.farm_selection_screen import FarmSelectionScreen
        FarmSelectionScreen(self.app)
