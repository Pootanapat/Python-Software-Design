import tkinter as tk
from tkinter import messagebox, ttk
from firebase_config import db
from utils import check_permission, add_log

class FarmSelectionScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title_label = tk.Label(self.frame, text="MINIFARM", font=("Arial", 20, "bold"), bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=20)

        subtitle_label = tk.Label(self.frame, text="Manage Your Farms", font=("Arial", 16), bg="#f5f5f5", fg="#7f8c8d")
        subtitle_label.pack(pady=10)

        # ปุ่มสร้างฟาร์มใหม่
        create_btn = tk.Button(self.frame, text="➕ Create New Farm", font=("Arial", 12, "bold"), bg="#3498db", fg="white", relief="flat", width=25, height=2, command=self.go_to_create)
        create_btn.pack(pady=10)
        create_btn.bind("<Enter>", lambda e: create_btn.config(bg="#2980b9"))
        create_btn.bind("<Leave>", lambda e: create_btn.config(bg="#3498db"))

        # ปุ่มเข้าร่วมฟาร์ม
        join_btn = tk.Button(self.frame, text="🤝 Join Farm", font=("Arial", 12, "bold"), bg="#9b59b6", fg="white", relief="flat", width=25, height=2, command=self.go_to_join)
        join_btn.pack(pady=10)
        join_btn.bind("<Enter>", lambda e: join_btn.config(bg="#8e44ad"))
        join_btn.bind("<Leave>", lambda e: join_btn.config(bg="#9b59b6"))

        # แสดงฟาร์มที่มีอยู่
        tk.Label(self.frame, text="Your Farms", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=10)

        # สร้าง Treeview และ Style
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        self.style.configure("Treeview", font=("Arial", 12))

        # ใช้ Treeview แทน Listbox เพื่อให้ดูสวยงามและมีโครงสร้าง
        columns = ("farm_name",)
        self.farm_tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=6)
        
        # กำหนดหัวคอลัมน์
        self.farm_tree.heading("farm_name", text="Farm Name")
        self.farm_tree.column("farm_name", width=250, anchor="w")

        # ใส่ Treeview ลงในหน้าจอ
        self.farm_tree.pack(pady=5, padx=20, fill="x")

        # ปุ่ม Select Farm
        select_btn = tk.Button(self.frame, text="✅ Select Farm", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", relief="flat", width=15, command=self.select_farm)
        select_btn.pack(pady=5)
        select_btn.bind("<Enter>", lambda e: select_btn.config(bg="#27ae60"))
        select_btn.bind("<Leave>", lambda e: select_btn.config(bg="#2ecc71"))

        # ปุ่ม Delete Farm
        delete_btn = tk.Button(self.frame, text="🗑️ Delete Selected", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", relief="flat", width=15, command=self.delete_farm)
        delete_btn.pack(pady=5)
        delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#c0392b"))
        delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#e74c3c"))

        # ปุ่ม Logout
        logout_btn = tk.Button(self.frame, text="🚪 Logout", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", relief="flat", width=15, command=self.logout)
        logout_btn.pack(pady=10)
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#c0392b"))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg="#e74c3c"))

        self.load_farms()

    def load_farms(self):
        # ลบข้อมูลเก่า
        for item in self.farm_tree.get_children():
            self.farm_tree.delete(item)

        user_id = self.app.current_user['localId']
        try:
            farms = db.child("users").child(user_id).child("farms").get()
            if farms.each():
                for farm in farms.each():
                    name = farm.val()["name"]
                    self.farm_tree.insert("", tk.END, values=(name,))
            else:
                self.farm_tree.insert("", tk.END, values=("No farms found",))
        except Exception as e:
            messagebox.showerror("Error", f"Could not load farms: {str(e)}")

    def select_farm(self):
        selected_item = self.farm_tree.selection()
        if selected_item:
            item_values = self.farm_tree.item(selected_item, "values")
            farm_name = item_values[0]
            try:
                # หา farm_id จากชื่อฟาร์ม
                farms = db.child("users").child(self.app.current_user['localId']).child("farms").get()
                for farm in farms.each():
                    if farm.val()["name"] == farm_name:
                        farm_id = farm.key()
                        break
                self.app.current_farm = farm_id
                from screens.farm_dashboard import FarmDashboardScreen
                self.app.clear_window()
                FarmDashboardScreen(self.app)
            except Exception as e:
                messagebox.showerror("Error", f"Could not select farm: {str(e)}")

    def delete_farm(self):
        selected_item = self.farm_tree.selection()
        if selected_item:
            item_values = self.farm_tree.item(selected_item, "values")
            farm_name = item_values[0]
            user_id = self.app.current_user['localId']
            try:
                # หา farm_id จากชื่อฟาร์ม
                farms = db.child("users").child(user_id).child("farms").get()
                for farm in farms.each():
                    if farm.val()["name"] == farm_name:
                        farm_id = farm.key()
                        break
                # ตรวจสอบว่าผู้ใช้เป็นเจ้าของหรือไม่
                owner = db.child("farms").child(farm_id).child("owner").get().val()
                if owner != user_id:
                    messagebox.showwarning("Permission Denied", "You are not the owner of this farm.")
                    return
                # ยืนยันการลบ
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{farm_name}'? This action cannot be undone.")
                if confirm:
                    # ลบออกจาก users/{user_id}/farms
                    db.child("users").child(user_id).child("farms").child(farm_id).remove()
                    # ลบออกจาก farms
                    db.child("farms").child(farm_id).remove()
                    add_log(farm_id, user_id, "deleted_farm", {"name": farm_name})
                    messagebox.showinfo("Success", f"Farm '{farm_name}' deleted successfully!")
                    self.load_farms()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete farm: {str(e)}")

    def go_to_create(self):
        self.app.clear_window()
        from screens.create_farm_screen import CreateFarmScreen
        CreateFarmScreen(self.app)

    def go_to_join(self):
        self.app.clear_window()
        from screens.join_farm_screen import JoinFarmScreen
        JoinFarmScreen(self.app)

    def logout(self):
        self.app.current_user = None
        self.app.current_farm = None
        self.app.clear_window()
        from screens.login_screen import LoginScreen
        LoginScreen(self.app)