import tkinter as tk
from tkinter import messagebox, ttk
from firebase_config import db
from utils import add_log

class RolePermissionScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title_label = tk.Label(self.frame, text="Manage Members", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=20)

        # สร้าง Treeview สำหรับแสดงสมาชิก
        columns = ("user_id", "role")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=8)
        
        # กำหนดหัวคอลัมน์
        self.tree.heading("user_id", text="User ID")
        self.tree.heading("role", text="Role")

        # กำหนดความกว้างของคอลัมน์
        self.tree.column("user_id", width=200, anchor="w")
        self.tree.column("role", width=150, anchor="center")

        # ใส่ Treeview ลงในหน้าจอ
        self.tree.pack(pady=10, fill="x", padx=20)

        # ปุ่ม Set Role
        role_btn = tk.Button(self.frame, text="⚙️ Set Role", font=("Arial", 10, "bold"), bg="#f39c12", fg="white", relief="flat", width=15, command=self.set_role)
        role_btn.pack(pady=5)
        role_btn.bind("<Enter>", lambda e: role_btn.config(bg="#d35400"))
        role_btn.bind("<Leave>", lambda e: role_btn.config(bg="#f39c12"))

        # ปุ่ม Back
        back_btn = tk.Button(self.frame, text="← Back", font=("Arial", 10, "bold"), bg="#95a5a6", fg="white", relief="flat", width=10, command=self.go_back)
        back_btn.pack(pady=20)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#7f8c8d"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#95a5a6"))

        self.load_members()

    def load_members(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            members = db.child("farms").child(self.app.current_farm).child("members").get()
            if members.each():
                for member in members.each():
                    user_id = member.key()
                    role = member.val()
                    self.tree.insert("", tk.END, values=(user_id, role))
            else:
                self.tree.insert("", tk.END, values=("No members found", "", ""))
        except Exception as e:
            messagebox.showerror("Error", f"Could not load members: {str(e)}")

    def set_role(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            user_id = item_values[0]
            role = item_values[1]

            # สร้างหน้าต่างเลือกบทบาท
            role_window = tk.Toplevel(self.app.root)
            role_window.title("Set Role")
            role_window.geometry("250x200")
            role_window.resizable(False, False)

            tk.Label(role_window, text="Select Role", font=("Arial", 12)).pack(pady=10)

            role_var = tk.StringVar(value=role)
            roles = ["owner", "animal_manager", "plant_manager", "viewer", "no_role"]
            for r in roles:
                tk.Radiobutton(role_window, text=r.replace("_", " ").title(), variable=role_var, value=r).pack(anchor="w", padx=30)

            def update_role():
                new_role = role_var.get()
                try:
                    db.child("farms").child(self.app.current_farm).child("members").child(user_id).set(new_role)
                    add_log(self.app.current_farm, self.app.current_user['localId'], "updated_member_role", {"user_id": user_id, "role": new_role})
                    messagebox.showinfo("Success", f"Role updated to {new_role} for {user_id}")
                    role_window.destroy()
                    self.load_members()
                except Exception as e:
                    messagebox.showerror("Error", f"Could not update role: {str(e)}")

            tk.Button(role_window, text="Update", command=update_role).pack(pady=10)
            tk.Button(role_window, text="Cancel", command=role_window.destroy).pack(pady=5)

    def go_back(self):
        self.app.clear_window()
        from screens.manager_screen import ManagerScreen
        ManagerScreen(self.app)